import java.util.Iterator;

public class Stack<Item> implements Iterable<Item>
{
    private class Node
    {
        public Item item;
        public Node next;
    }

    public push(item)
    {
        first = current;
        Node current = new Node();
        current.next = first;
        first = current;
    }

    public Item pop()
    {
    }

    public Iterator<Item> iterator() { return new ListIterator(); }

    private class ListIterator implements Iterator<Item>
    {
        private Node current = first;

        public boolean hasNext() { return current != null; }
        public void remove() { }
        public Item next()
        {
            Item item = current.item;
            current = current.next;
            return item;
        }
    }
}

