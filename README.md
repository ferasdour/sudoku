# Sudoku Rabbit Hole

This all started with sucking at sudoku and wanting to learn tricks to be better, so show off for my wife. 

Question: How is sudoku boards made
Answer: put numbers around that fit a board correctly, then take some off, and ensure none of the "deadly patterns" exist.

So of course, lets make sudoku with multiple variants and just see how many can be generated in total:

![](./Pasted%20image%2020260516201033.png)

So now I can hash those boards and anything matching those hashes is definitely duplicate.

Now I can create a math solution:

![](./Pasted%20image%2020260516201918.png)

So I went ahead and also made a generator that could make the hash values of the grid with . and with 0 in place of empty spots for the array.

![](./Pasted%20image%2020260516204935.png)

I also went ahead and got a script made (google) to generate these deadly patterns

![](./Pasted%20image%2020260516204856.png)

Nothing remarkably interesting here, just an experiment or 3. 
