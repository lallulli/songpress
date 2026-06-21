# Format conversion

## Tab format to Chordpro

Songpress can convert songs from the "tab" format to the Chordpro format.

In the "tab" format, chords are placed above text, in separate lines:

```
C              F        C
My Bonnie lies over the ocean
C              F        G
My Bonnie lies over the sea...
```

To convert a single chord line to ChordPro, place the cursor on the chord line and select **Edit -> Integrate chords**.

To convert the whole song, or a selection, use **Tools -> Convert Tab to Chordpro**.


## Songs with spurious blank lines

It is quite common to find songs, either in the Chordpro or (more often) in the "tab" format, with some spurious blank lines inside. Sometimes this happens when you copy-paste a song. For example:

```
C              F        C
My Bonnie lies over the ocean
                               (this is a "spurious" blank line)
C              F        G
My Bonnie lies over the sea...
```

You should remove all the blank lines, except those separating two verses. Luckily, Songpress can do this for you. Just select **Tools -> Remove spurious blank lines**.

!!! warning "Remember"
    If the song is in the "tab" format, first remove spurious blank lines (if any); after that, convert the song to Chordpro.


## AutoAdjust

Songpress is able to detect if a song has spurious blank lines, or if it is in the "tab" format, and convert it to clean Chordpro automatically (after asking for confirmation, of course). This feature is called AutoAdjust and is active by default; should you want to turn it off, go to **Tools -> Options**.
