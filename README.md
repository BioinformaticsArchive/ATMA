ATMA project
=================
ATMA (Automated Tracer for Myelinated Axons) is a user-friendly tool for interactive reconstruction of the geometry of fibers inside a peripheral nerve on its high resolution serial section images. Another feature of ATMA is the automatic detection of the nodes of Ranvier within this nerve.
Most analysis operations are performed on a data sub-volume, followed by complete volume analysis in batch mode. Using it requires no experience in machine learning or image processing.

Key Words:
Integer Linear Programing, Hungarian Algorithm, Random Forest, Union Finder, Image Analysis


Install
-------
Check out the latest version with the command:
```bash
    git clone git@github.com:RWalecki/ATMA.git
```



Quick Start (GUI)
-----------
Run the ATMA GUI:
```bash
"cd ATMA"
"./run.sh"
```

1. Select Volume by clicking on 'Load Raw/Prediction Data'.
2. Set range of sub volume (should not be larger than 1000*1000*1000 voxel).
![ATMA-GUI](https://github.com/RWalecki/ATMA/blob/master/doc/01_Prediction.png?raw=true)

3. Enter initial parameter and run Axon Classification.
![ATMA-GUI](https://github.com/RWalecki/ATMA/blob/master/doc/02_AxonClassification.png?raw=true)

4. Train Node Classifier. The "Zoom-in/out" button triggers the node-view.
![ATMA-GUI](https://github.com/RWalecki/ATMA/blob/master/doc/03_NodeDetection.png?raw=true)
This image below shows a node of Ranvier (left) and a gap that occurs due to under-segmentation (right). 
![ATMA-GUI](https://github.com/RWalecki/ATMA/blob/master/doc/04_Nodes.png?raw=true)
5. Apply Batch Processing. The complete volume will be processed using the previously obtained parameters for classification (step 3) and the recently trained classifier for node of Ranvier detection (step 4).

Quick Start (CLT)
-----------
ATMA contains additional methods for axon segmentation and axon classification that are not implemented in the GUI version. These methods can be executed directly from the source code.
(Note: do not forget to add the folder that contains ATMA to your PYTHONPATH)

```python
import ATMA
import h5py


pred = h5py.File("./test.h5")["volume/data"]

#SEGMENTATION
a=ATMA.Segmentation.BioData.Nerve( pred )
a.sigmaSmooth = 0.7
a.thresMembra = 0.7
a.sizeFilter = [20,1000]
a.run()
Axon_bin = a.seg


#Gap Closing
b=GapClosing.Tokenizer.Data2Token( Axon_bin )
b.minSize = 3000
b.run()
Axon_id = b.data
```


Testing
-------
```bash
nosetests 
```


REQUIREMENTS (CLT)
------------------

* Python (tested with 2.7.4)
* numpy (tested with 1.7.1)
* vigra (tested with 1.8.0)
* h5py (tested with 2.2.0b1)
* munkres (tested with 1.0.6)

ADDITIONAL REQUIREMENTS FOR GUI VERSION
---------------------------------------
* PyQt4 (tested with 4.10.3)
* MayaVi (tested with 4.3.0)
