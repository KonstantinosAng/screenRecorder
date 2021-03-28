# Screen Recorder

A simple screen recorder app made with [ElectronJS](https://www.electronjs.org/) and with [Python](https://www.python.org) too.

## Electron version

The [screenRecorder folder](./screenRecorder/) contains the electron app. Assuming you have [npm](https://www.npmjs.com) installed, clone the repo, go inside the [screenRecorder folder](./screenRecorder/) and run the following code:

```
npm i && npm start
```

To build the .exe file for your own OS run the following code:

```
npm run make
```

## Python version

Python version lacks a gui for now and lacks audio capture.
See at the end of the [main python file](./screenRecorder-python/src/record.py) for usage.

## Examples

Electron app
<br>
<p align="center">
  <img src="img/electron.png" />
</p>
