Riverside.fm Transcripts Merger
===

In case you have more recordings, part of the same episode, you end up with a bunch of transcripts.

We needed to have one single transcript file with the right timestamps, so that we can leverage LLMs to summarise and extract quotes with timestamp.

The transcript format is simple, take a look in the `samples` folder.

# How to run


```
# Run the existing samples to get the feel of how it works.
python merger.py samples

# Use the default path: (`transcripts` folder) to find all transcript files ordered alphabetically.
python merger.py

# Use whatever other path to get the transcript files sorted alphabetically.
python merger.py /tmp/transcripts
```

This script expects *.txt transcripts in a folder as Riverside.fm provides. 
