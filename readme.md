# Setup

First, make sure that all python dependencies are installed: `[sudo] pip install -r requirements.txt` (run without sudo on Windows)

## Install essentia extractors

### Ubuntu
  * `cd ~/ && wget http://essentia.upf.edu/documentation/extractors/essentia-extractors-v2.1_beta2-linux-x86_64.tar.gz`
  * `tar xzf essentia-extractors-v2.1_beta2-linux-x86_64.tar.gz`
  * `echo 'PATH=~/essentia-extractors-v2.1_beta2/:$PATH' >> ~/.bashrc`
  * `source ~/.bashrc`

### Windows
* Download tar for windows at http://essentia.upf.edu/documentation/extractors/
* Extract and add to the PATH variable

# Usage

Place a file `features.json` in the input folder. It should contain settings about which files to analyze and which features to use for each file. Example:
```json
{
  "flute.wav": [
    "spectral_energy",
    "spectral_centroid"
  ],
  "hihat.wav": [
    "spectral_energy"
  ]
}
```

Wav files referenced in the `features.json` file should reside in the same folder. They should have the following format:
* Number of channels: 1 (mono) or 2 (stereo)
* Sampling rate: 44100 Hz
* Bit depth: 16 or 32

Now run `python analyzer.py` and wait. It should create a file `audioAnalysis.js` in the input folder.
