public class Percolation {
    private int top, bottom, seed;
    public WeightedQuickUnionUF grid;
    public int[] state;
    
    public Percolation(int N) {
        seed = N;
        int sz = N*N;
        top = 0; bottom = sz+1;
        grid = new WeightedQuickUnionUF(sz+2);
        
        state = new int[sz+2];
        state[0] = 1; state[bottom] = 1;
        
        for (int i=1; i<=N; i++) grid.union(0,i);
        for (int i=bottom-N; i<=bottom-1; i++) grid.union(bottom, i);
    }
    
    private int position(int row, int col) {
        int base = row * seed;
        int diff = seed - col;
        return base - diff;
    }
    
    public boolean isOpen(int row, int col) {
        int pos = position(row, col);
        return state[pos] == 1;
    }
    
    public boolean isFull(int row, int col) {
        int pos = position(row, col);
        if (isOpen(row, col))
            return grid.connected(0,pos);
        else
            return false;
    }
    
    public boolean percolates() {
        return grid.connected(0,bottom);
    }
    
    public void open(int row, int col) {
        if (row > seed || col > seed) throw new IllegalArgumentException();
        
        int base = row * seed;
        int diff = seed - col;
        
        int pos = position(row, col);
        state[pos] = 1;

        if (row < seed) {
            int _base = (row+1) * seed;
            int _pos = _base - diff;
            if (state[_pos] == 1) grid.union(pos, _pos);
        }
        
        if (row > 1) {
            int _base = (row-1) * seed;
            int _pos = _base - diff;
            if (state[_pos] == 1) grid.union(pos, _pos);
        }
        
        if (col > 1 && col != 5) {
            int _diff = seed - (col+1);
            int _pos = base - _diff;
            if (state[_pos] == 1) grid.union(pos, _pos);
        }
        
        if (col < seed && col != 1) {
            int _diff = seed - (col-1);
            int _pos = base - _diff;
            if (state[_pos] == 1) grid.union(pos, _pos);
        }
    }
    
}