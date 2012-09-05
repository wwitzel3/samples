public class PercolationStats {
    private int _T;
    private int size;
    
    public PercolationStats(int N, int T) {
        if (N <= 0 || T <= 0) throw new IllegalArgumentException();
        _T = T;
        size = N;
    }
    
    public double mean() {
        Percolation p = new Percolation(size);
        double sum = 0;
        for (int i=0; i<_T; i++) {
            while (!p.percolates())
                p.open(StdRandom.uniform(1,size+1), StdRandom.uniform(1,size+1));
            sum += p.openCount() / (size*size);
        }
        return sum / _T;
    }
    
    public double stddev() {
        Percolation p = new Percolation(size);
        double _mean = mean();
        double sum = 0;
        for (int i=0; i<_T; i++) {
            while (!p.percolates())
                p.open(StdRandom.uniform(1,size+1), StdRandom.uniform(1,size+1));
            double _total = (p.openCount() / (size*size)) - _mean;
            sum += Math.pow(_total, 2);
        }
        return sum / _T-1;
    }
    
    public static void main(String[] args) {
        PercolationStats ps = new PercolationStats(200,100);
        
        double _stddev = ps.stddev();
        double _mean = ps.mean();
        
        StdOut.printf("mean                    = %f\n", _mean);
        StdOut.printf("stddev                  = %f\n", _stddev);
        
        double interval_a = _mean - ((1.96*_stddev) / Math.sqrt(100));
        double interval_b = _mean + ((1.96*_stddev) / Math.sqrt(100));
        
        StdOut.printf("95%% confidence interval = %.10f, %.10f\n",
                      interval_a, interval_b);
    }
}