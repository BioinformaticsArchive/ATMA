ATMA project
=================
ATMA (Automated Tracer for Myelinated Axons) is a programm for detailed reconstruction of the geometry of fibers inside a peripheral nerve based on its high resolution serial section images and for the detection of the nodes of Ranvier within this nerve.

![ATMA-GUI](https://github.com/RWalecki/ATMA/blob/master/doc/screenshot.png?raw=true)

Install
-------
You can check the latest sources with the command::

    git clone git@github.com:RWalecki/ATMA.git



USAGE 
-----

The GUI version can be executed by running the script 

```bash
"./run.sh"
```

ATMA contains several methods for segmentation, tracing and classification. These methods can be run directly in python.
(Note: do not forget to add ATMA to your PYTHONPATH)
Here a short example:

```python
import ATMA
import h5py


pred = h5py.File("./test.h5")["volume/data"]

#SEGMENTATION
a=ATMA.src.Segmentation.BioData.Nerve( pred )
a.sigmaSmooth = 0.7
a.thresMembra = 0.7
a.sizeFilter = [20,1000]
a.run()
seg = a.seg


#Gap Closing
#...
#...

#Node Detection
#...
#...
```



Testing
-------
After installation, you can launch the test suite from outside the
source directory (you will need to have nosetests installed)::

   $ nosetests 


REQUIREMENTS
------------

* Python (tested with 2.7.4)
* numpy (tested with 1.7.1)
* vigra (tested with 1.8.0)
* PyQt4 (tested with 4.10.3)
* MayaVi (tested with 4.3.0)
* h5py (tested with 2.2.0b1)
