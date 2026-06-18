# Transposing and changing notation

Songpress can transpose songs, and change chord notation. For example, it can read Italian-style chords, used in latin countries (such as Do, Re-, Sol7+) and translate them in American-style chords (like C, Dm, Gmaj7).


## Transposing

In order to transpose the entire song, select **Tools -> Transpose**. In order to transpose a portion of the song, select the portion and then select **Tools -> Transpose**.

Songpress will try to detect the notation of the song, and the current key. Please make sure they are correct.

Then select either the gap, in semitones, between the current key and the key you want to transpose your song in; or the destination key. Press OK.

As a side note, you may ask why you need to specify current and destination key. Wouldn't be enough to set the gap in semitones? The reason is that the correct notation of chords depends on the song key. For example, if the key is F the correct notation of "A#" is Bb; but if the key is B, the correct notation of A# is actually A#. For this reason, if the song you are transposing is made of several section having different keys, each section should be transposed separately.

!!! note "# and b saga"
    It is not only a matter of notation: A# and Bb are actually different, but very similar chords. In instruments where the pitch of sounds is discretized, such as piano or guitar, an intermediate pitch between A# and Bb is used for both of them. But in instruments, like violin, that can produce a continuous range of pitches, the chords should be played differently.

## Changing chord notation

In order to modify the chord notation of the entire song, select **Tools -> Change chord notation**. If you want to change the notation of a portion of the song, select it and then select **Tools -> Change chord notation**.

Songpress will try to detect the current notation of the song. Make sure it is correct, select the destination notation and press OK.
