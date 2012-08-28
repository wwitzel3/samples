public class QuickUnionWeighted
{
    private int id[];
    private int sz[];

    public QuickUnion(int N)
    {
       id = new int[N];
       for (int i=0; i<N; i++)
       {
           sz[i] = 0;
           id[i] = i;
       }
    }

    private int root(int i)
    {
        while (i != id[i])
        {
            id[i] = id[id[i]];
            i = id[i];
        }
        return i;
    }

    public boolean connected(int p, int q)
    {
        return root(p) == root(q);
    }

    public void union(int p, int q)
    {
        int i = root(p);
        int j = root(q);
        if (sz[i] < sz[j]) { id[i] = j; sz[j] += sz[i]; }
        else { id[j] = i; sz[i] += sz[j]; }
    }
}

