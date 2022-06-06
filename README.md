# Worlds-Hardest-Game-AI

An self-learning AI I for the worlds hardest game. Includes a level editor. 

To play the game: run the WHG file. This is not specialised for human players so quality for this may be lacking
To watch the AI: Run the learningManager. Here you can edit the function at the bottom for changing maps, and other values
(note that generations is set to 1000 by default, but the program will cancel after reaching the goal)

To edit the level: run the levelCreator file. Here you can specify the file right at the top of the file. 
While most functions in the editor are self-explenatory the blobs are not: "Blobs" refers to the deadly orbs in the game. To create a new orb
select "Blobs" to edit. Each blob is defined by a set of points that it will follow through straigh lines and return to the start. All lines 
MUST be straight along the x or y axis including the return to the start. To create a new blob, press e and click somewhere. 
This creates the first point and furhter points in the path are added by subsequent clicks. 
You remove a blob using backspace and rotate through blobs using the arrow keys. 
Blobs not currently selected will only show their starting point, greyed out

To switch to circle mode, press c. These are the blobs that spin sround a point. Here you will first choose where the center of the circle is and then you will click again to determine the radius.
Exit circle mode with c. Circles created in circle mode are not higlighted.

Checkpoints serve as a guide to AI and it will only be able to learn fairly straight lines between checkpoints
