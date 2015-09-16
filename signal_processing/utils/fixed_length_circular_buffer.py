
class FixedLengthCircularBuffer(object):

    """
    The picture is this:

    array indices, given buf-len = 8:
     0    1     2     3     4     5     6     7     8

    rotating label indices:
     n-2   n-1   n    n-7   n-6   n-5   n-4   n-3
    -----------------------------------------------------
    |    |     |     |     |     |     |     |     |
    -----------------------------------------------------
                 ^                                   ^
                 |                                   |
              cursor                              buf_len


    on push(v):

     n-3   n-2   n-1   n    n-7   n-6   n-5   n-4
    -----------------------------------------------------
    |    |     |     |     |     |     |     |     |
    -----------------------------------------------------
                       ^
                       |
                    cursor

    INVARIANT: cursor points to rotating index /n/, which is index of the
               last-pushed value

    * push() advances the cursor and copies the push value v to the buffer
      at /cursor/
    * next() advances in the direction of push()
    * prev() goes in the opposite direction
    * next()/prev() returns the value pointed to by /iter/ *and then* moves iter


     n-3   n-2   n-1   n    n-7   n-6   n-5   n-4
    -----------------------------------------------------
    |    |     |     |     |     |     |     |     |
    -----------------------------------------------------
                       ^
                       |
            prev <--  iter  --> next

    Two points of reference are /first/ and /last/:

     n-3   n-2   n-1   n    n-7   n-6   n-5   n-4
    -----------------------------------------------------
    |    |     |     |     |     |     |     |     |
    -----------------------------------------------------
                       ^     ^
                       |     |
                     first  last

    Typical iterations:

      *) toFirst() follow by a sequence of prev() calls gives the sequence
          (n, n-1, ..., n-7)

      *) toLast() followed by a sequence of next() calls gives the sequence
          (n-7, n-6, ..., n)

    """

    def __init__(self, buffer_length):

        # buffer length, wraps around when indexed out of bounds
        self._len = buffer_length

        # setup the internal buf as a list
        self._buf = [0 for x in range(self._len)]

        # cursor position into the circbuf
        self._cursor = 0

        # iterator index into the circbuf
        self._iter = 0


    # refresh
    def reset(self):
        self._buf    = [0 for x in range(self._len)]
        self._cursor = 0

    # inspect
    def size(self):
        return self._len

    def end(self):
        return ((self._cursor + self._iter) % self._len) == 0

    # push / pop
    def push(self, v):
        self._cursor = self._increment(self._cursor)
        self._buf[self._cursor] = v

    def pop(self):
        v = self._buf[self._cursor]
        self._cursor = self._decrement(self._cursor)
        return v

    # access
    def toFirst(self):
        self._iter = self._cursor

    def first(self):
        return self._buf[self._cursor]

    def toLast(self):
        self._iter = self._increment(self._cursor)

    def last(self):
        return self._buf[self._increment(self._cursor)]

    def next(self):
        v = self._buf[self._iter]
        self._iter = self._increment(self._iter)
        return v

    def prev(self):
        v = self._buf[self._iter]
        self._iter = self._decrement(self._iter)
        return v

    # internals, reentrant -- no side effect
    def _increment(self, i):
        return (i+1) % self._len

    def _decrement(self, i):
        return (i + (self._len - 1)) % self._len
