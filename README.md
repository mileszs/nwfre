# NWFRE -> North Willow Farms Real Estate

NWFRE is a little Python script I wrote to analyze some real estate sales data
from my neighborhood, North Willow Farms, located in the northwest corner of
Indianapolis, Indiana, USA. We moved into the neighborhood in early 2014. I
thought it would be interesting to view some of the sales data from at least
around that time through to the present. Thankfully, I was able to find a
dataset that goes back to 2008! This also gives me the opportunity to further
experiment with Python, Pandas, Plotly, and other libraries—which was really my
primary motivation.

You can see the result at [mileszs.com/nwfre](https://www.mileszs.com/nwfre/)

## Dataset

Though the data itself is public record, I believe, I compiled and hand-filtered
the data using other sources. I have decided to keep the data itself out of this
repository, as it's not really mine. Related: The result of this script is
prohibited from use for commercial purposes to the extent that I can make that
true by saying it here. Any data exposed or other information cannot be resold.
The graphs themselves cannot be resold. If you're a neighbor of mine and wish to
use the result to inform how you list your house, or to justify adding a 5th
bedroom, etc, feel free! If you're a prospective neighbor and you want to
somehow use the data to make an offer on a house in NWF, feel free! Also let me
know, because we should walk the neighborhood with wine in hand, or something.

## Technical Junk

I used Python and Pandas, as one does with data. I've chosen Plotly for the
graphs, because I like the interactivity for this particular data set. I'm using
Jinja for the HTML template, which I have never heard of, but ChatGPT assured me
it was a good choice. I have also abandoned `requirements.txt` for Poetry, which
is more inline with my experience with Ruby's Bundler. (Python people: do you
actually just use requirements.txt in big projects? You don't, right? Surely
not. Please reassure me. Someone. Anyone.)

To play with this yourself, you can clone it, then `cd` into the root. Then:

```bash
poetry install
poetry run python generate.py
```

This assumes you have the proper JSON file in the `data/` directory, or a
reasonable facsimile.