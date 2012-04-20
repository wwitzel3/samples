#include <iostream>
#include <vector>
#include <boost/shared_ptr.hpp>
#include <boost/thread.hpp>
#include <boost/python.hpp>

class ScopedGILRelease {
public:
	inline ScopedGILRelease() { m_thread_state = PyEval_SaveThread(); }
	inline ~ScopedGILRelease() { PyEval_RestoreThread(m_thread_state); m_thread_state = NULL; }
private:
	PyThreadState* m_thread_state;
};

void loop(long count)
{
	while (count != 0) {
		count -= 1;
	}
	return;
}

void nogil(int threads, long count)
{
	if (threads <= 0 || count <= 0)
		return;
	
	ScopedGILRelease release_gil = ScopedGILRelease();
	long thread_count = (long)ceil(count / threads);
	
	std::vector<boost::shared_ptr<boost::thread> > v_threads;
	for (int i=0; i != threads; i++) {
		boost::shared_ptr<boost::thread> m_thread = boost::shared_ptr<boost::thread>(new boost::thread(boost::bind(loop,thread_count)));
		v_threads.push_back(m_thread);
	}
	
	for (int i=0; i != v_threads.size(); i++)
		v_threads[i]->join();
	
	return;
}

BOOST_PYTHON_MODULE(nogil)
{
	using namespace boost::python;
	def("nogil", nogil);
}
