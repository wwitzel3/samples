public class PercolationStats {
    private int _T;
    private int size;
    private Percolation p;
    
    public PercolationStats(int N, int T) {
        if (N <= 0 || T <= 0) throw new IllegalArgumentException();
        _T = T;
        size = N;
        p = new Percolation(N);
    }
    
    public double mean() {
        double sum = 0;
        for (int i=0; i<_T; i++) {
            int count = 0;
            while (!p.percolates()) {
                p.open(StdRandom.uniform(1,size+1), StdRandom.uniform(1,size+1));
                count++;
            }
            sum += count/_T;
        }
        System.out.println(sum);
        return sum / _T;
    }
    
    public static void main(String[] args) {
        PercolationStats ps = new PercolationStats(200,100);
        System.out.println(ps.mean());
    }
}