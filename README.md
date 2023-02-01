# Natural Language Processing for sentiment and topic recognition

The goal of this project is to be able to extract useful information (sentiment and topic for example) from single sentences instead of whole documents, without the need to possess already labeled data to use as a knowledge base, thus making use of unsupervised machine learning algorithms.<br>
Subsequently, this data will be used to create adaptive settings with stage effects, sound effects, and graphics that can stimulate viewers in stage and theater settings.<br>
This software also offers a web interface capable of simulating the above.

#### Requirements
* `django`
* `django rest framework`
* `nltk`
* `gensim`
* `pandas`
* `numpy`

## How to start it
```sh
docker build -t webapp .
```

```sh
docker run -dt 8000:8000 webapp 
```

## Web interface 

### Output with topic: Nature and sentiment: Positive
<p align='center'>
<img src="pictures/Web interface nature positive.png">
</p>

### Output with topic: Nature and sentiment: Negative
<p align='center'>
<img src="pictures/Web interface nature negative.png">
</p>
