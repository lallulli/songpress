# Autodetecting song key

One of the new features in the upcoming 1.1 release of [Songpress](../index.md) is song transposition. In order do transpose the right way, we need to know the current key of the song (or of the part of it we want to transpose), and the destination key (or, equivalently, the gap between the source and destination key, expressed in semitones).

Thus I decided to experiment an algorithm to "guess" the current key of the song, by examining the song chords. The basic idea is simple: each key has its own "natural" chords. For example, in songs on the C key the most frequently occurring chords are C, F, G, Am, Dm, Em, E, sometimes A and D, etc. Then, if we count the number of occurrences of each type of chord, we obtain a sort of "footprint" of the song, that we can compare with reference "footprints" of every possible key. And we select the key of the most similar "footprint".

The idea is simple but somewhat vague; the full algorithm is as simple as the idea. All you need to know is the basics of linear algebra.

If you count the number of occurrences of each type of chord in a song, you get a vector. We decided to consider, as chord types, the major, minor, seventh and minor seventh modes of each tone of the chromatic scale. Thus the components of our song vectors are the number of occurrences of the following chord types: C, Cm, C7, Cm7, C#, C#m, C#7, C#m7, D, Dm, ..., B, Bm, B7, Bm7. The vector has 12*4 = 48 components.

Now, let's normalize the song vector. We get a versor whose direction is related to the key of the song: we expect that all the songs on a given key roughly share the same versor. Thus, all we need to know is the versor of each key. We consider a reference set of songs on the C key (in practice, I used our [songbook of the Holy Mass](http://www.roma21.it/assets/Download/CantiMessaCRD.zip): I discarded some irregular song and transposed all the others to the C key); concatenate them and compute the versor of the resulting "song". Thus we get the reference "C / Am" versor. By a simple rotation of it, we can get the versors of all the other 11 keys.

To determine the key of a song, we compute the song versor v, and compare it with the 12 key versors: simply compute the scalar product of v by each of the key versors, and select the maximum.

For the sake of curiosity, here is the reference "C / Am" versor (rounded to 2 digits for the sake of readability):


Chord | Major | Minor | 7 | Minor 7
------| ----- | ----- | - | ------
C | 0,66 | 0 | 0,04 | 0
C# | 0 | 0 | 0 | 0
D | 0,03 | 0,12 | 0 | 0,03
D# | 0 | 0 | 0 | 0
E | 0,04 | 0,13 | 0,03 | 0
F | 0,46 | 0,01 | 0 | 0
F# | 0 | 0 | 0 | 0
G | 0,5 | 0 | 0,02 | 0
G# | 0 | 0 | 0 | 0
A | 0,01 | 0,26 | 0,01 | 0
A# | 0 | 0 | 0 | 0
B | 0 | 0 | 0 | 0


How well does this algorithm work? Incredibly well on my song set:

- I bootstrapped the algorithm with only ONE reference song, and used it to transpose the first half of my song set (approx. 30 out of 60 songs): the algorithm failed on 4 songs only;
- I updated the reference versor using the first half of the set; I ran the algorithm again on the 4 failing songs, and only 1 of them was still failing;
- I completed the transposition of the reference set with no further fails, and updated the reference versor again.
- Finally, I tested the fully-calibrated algorithm on another set of songs ([cub scout songs](http://www.roma21.it/assets/Download/FioreRosso/crd.zip)), and I got only 1 fail on them.

It is interesting to observe that the 2 failed songs are "strongly" minor songs in Am, where the only chords are Am, Dm and E; the algorithm thinks their key is E / C#m (because E is the only major chord in the song, and it is given a strong weight in the scalar product with the E / C#m versor by its E component). Perhaps we could try to generate a set of reference versors for the "strongly" minor songs.