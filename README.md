# handwritten-digits-corpus
This is a small corpus of handwritten digits.

It contains the sequential writing data of five individuals, tasked to write all ten digits (0-9) as they would naturally.
Each individual was tasked to write digits as asked, with digits being randomly selected, with a total of ten repetitions per digit.
The writing was captured in a specifically created iOS App, on a 6th generation iPad, using a first-generation Apple Pencil.



Contained in this repository is the corpus data itself, along with a sample Python script for reading out the handwriting data.
Specifically, two versions of the corpus are included. One is the unfiltered corpus, as it was recorded. From the filtered version, I excluded individual drawings that either contained interrupted drawings, wrong drawings (e.g., a drawn 9, when a 1 was asked for).

The corpus is stored in JSON format, with a structure as follows:
```json
{
    digit (0-9): {
        user-id [1,2,4,5,6]: {
            repetition (0-9): 
            [
                for each movement coordinate
                {
                    start-coordinate "start": {
                        "x": float,
                        "y": float
                    },
                    end-coordinate "end": {
                        "x": float,
                        "y": float
                    },
                    absolute timestamp "time": float
                }
            ]
        }
    }
}
```

Also, under the corpus_plots folder, each individuals drawings were plotted.
As you see, the corpus from individual 6 had to be heavily filtered. Also the drawings from that user have been written at very low speeds, which resulted in lots of noise. This data is still included, but should not be used for training, as it can heavily offset previous training.


This corpus was previously used for training the https://github.com/skahl/hpbu model.

Have fun!
