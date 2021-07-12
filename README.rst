Click the button below to launch a Binder session:

.. image:: https://mybinder.org/badge.svg
   :target: https://mybinder.org/v2/gh/sametz/chem333/cleanup

The notebooks of interest to CHEM333 students are:

- first_order_part_1.ipynb: describes first-order splittings that follow the
  "*n* + 1" rule
- first_order_part_2.ipynb: describes non-"*n* + 1" first order splittings,
  e.g. double of doublets (dd), doublet of doublet of doublets (ddd), etc.
- second_order.ipynb: describes second-order splittings.

The easiest way to use the notebook
is to click the "launch binder" icon above.
There will be a loading animation displayed,
with a facsimile of a file directory beneath.
When the loading animation is done,
you should be left with a functioning file directory.
Clicking on one of the files listed above
should launch the Jupyter notebook in a new browser tab.

In the notebook,  select "Run All"
from the "Cell" dropdown menu at the top of the page.
This will run all the code in the notebook
and generate interactive NMR plots.
The tutorial includes directions
for how to manipulate the plots and observe the results.

Feel free to change parameters, or even the code itself,
to see what happens--you can't break anything.
Near the start of each document is a link you can click
to toggle revealing/hiding the code behind the simulations.
If you need to restore a simulation to the initial slider settings,
you can click inside the code cell for the plot
and hit shift-return to re-load it.
If you want to reload the entire notebook
(e.g. you accidentally typed in a code block
and don't know how to fix it),
select "Restart & Run All" from the "Kernel" menu.

If you are already familiar with Jupyter notebooks,
you can of course download the files and run them on your own computer.
The requirements.txt has the list of necessary Python packages.
Any Python version >= 3.6 should work.
It's strongly recommended to use a virtual environment
(or, if you use a conda/Anaconda installation, a conda environment) for this.
