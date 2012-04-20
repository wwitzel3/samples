GAAlleleSet<int> get_volunteer_alleles(std::map<int, GAVolunteer>* volunteers) {
	GAAlleleSet<int> alleles;
	for(std::map<int, GAVolunteer>::const_iterator i = volunteers->begin(); i != volunteers->end(); i++) {
		alleles.add(i->first);
	}
	alleles.add(None);
	return alleles;
}

boost::python::list ga_eval(boost::python::list& event_list, boost::python::list& volunteer_list,
		int gatype=2, int popsize=150, int ngen=600, float pmut=0.01, float pcross=0.9) {

	boost::python::stl_input_iterator<GAEvent> gae_begin(event_list), gae_end;
	events = new std::vector<GAEvent>;
	for (;!(gae_begin.equal(gae_end)); gae_begin++) { events->push_back(*(gae_begin)); }
	boost::python::stl_input_iterator<GAVolunteer> gav_begin(volunteer_list), gav_end;
	volunteers = new std::map<int, GAVolunteer>;
	for (;!(gav_begin.equal(gav_end)); gav_begin++) {
		GAVolunteer volunteer = static_cast<GAVolunteer>(*(gav_begin));
		(*volunteers)[volunteer.id] = volunteer;
	}
	// DO IT HERE
	GAAlleleSetArray<int> volunteer_alleles = get_volunteer_alleles(events, volunteers);
	GA1DArrayAlleleGenome<int> genome(volunteer_alleles, objective);
	GAGeneticAlgorithm *ga;

	switch (gatype) {
	case 1: {
		ga = new GASimpleGA(genome);
		ga->populationSize(popsize);
		ga->nGenerations(ngen);
		ga->pMutation(pmut);
		ga->pCrossover(pcross);

		GATournamentSelector selector;
		ga->selector(selector);
		break;
	}
	case 2:
		ga = new GASteadyStateGA(genome);
		ga->populationSize(popsize);
		ga->nGenerations(ngen);
		break;
	default:
		ga = new GASteadyStateGA(genome);
		ga->populationSize(popsize);
		ga->nGenerations(ngen);
	}

	ga->evolve();
	// DO IT HERE

	delete events;
	delete volunteers;

	boost::python::list results;

	const GA1DArrayAlleleGenome<int>& genome_results = (GA1DArrayAlleleGenome<int>&)ga->statistics().bestIndividual();
	for(unsigned int i=0; i != (unsigned int)genome_results.length(); i++) { results.append(genome_results[i]); }

	delete ga;

	return results;
}

BOOST_PYTHON_MODULE(nnga)
{
    using namespace boost::python;

	class_<GAVolunteer>("GAVolunteer", init<int, bool, float, int, bool, bool, float, int>())
		.def_readwrite("vacations", &GAVolunteer::vacations)
		.def_readwrite("availabilities", &GAVolunteer::availabilities)
		.def_readwrite("assignments", &GAVolunteer::assignments)
	;

	class_<GAEvent>("GAEvent", init<int, int, int, float, int, float, float,
			int, int, int, int, int, int, float>())
		.def_readonly("volunteers_needed", &GAEvent::volunteers_needed)
		.def_readonly("id", &GAEvent::id)
	;

    def("ga_eval", ga_eval);

    class_<GAAssignment>("GAAssignment", init<GAEvent&, bool>());
    class_<GAAvailability>("GAAvailability", init<int, int>());
    class_<GAVacation>("GAVacation", init<float, float>());

    class_<Assignments>("Assignments")
		.def("append", &Assignments::push_back)
	;
	class_<Availabilities>("Availabilities")
		.def("append", &Availabilities::push_back)
	;
	class_<Vacations>("Vacations")
		.def("append", &Vacations::push_back)
	;
}