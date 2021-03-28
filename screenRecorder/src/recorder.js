const videoRoot = document.getElementById('video__root');
const startButton = document.getElementById('start__button');
const stopButton = document.getElementById('stop__button');
const videoSelectButton = document.getElementById('video__select__button');

const { desktopCapturer, remote } = require('electron');
const { Menu, dialog } = remote;

let mediaRecorder;
const recordedChunks = [];
const { writeFile } = require('fs');


videoSelectButton.onclick = getVideoSources;

stopButton.onclick = (event) => {
  mediaRecorder.stop();
  startButton.innerText = 'Start';
}

startButton.onclick = (event) => {
  mediaRecorder.start();
  startButton.innerText = 'Recording...';
}

async function getVideoSources() {

  const inputSources = await desktopCapturer.getSources({
    types: ['window', 'screen']
  });
  
  const videoOptionsMenu = Menu.buildFromTemplate(
    inputSources.map(source => {
      return {
        label: source.name,
        click: () => selectSource(source)
      }
    })
  )
  videoOptionsMenu.popup();
}

async function selectSource(source) {
  videoSelectButton.innerText = source.name;

  const constraints = {
    audio: {
      mandatory: {
          chromeMediaSource: 'desktop',
          chromeMediaSourceId: source.id
      },
      optional: [
        {sampleRate: 48000},
        {volume: 1.0},
        {channelCount: 2},
        {googAutoGainControl: false},
        {googAutoGainControl2: false},
        {echoCancellation: false},
        {googEchoCancellation: false},
        {googEchoCancellation2: false},
        {googDAEchoCancellation: false},
        {googNoiseSuppression: false},
        {googNoiseSuppression2: false},
        {googHighpassFilter: false},
        {googTypingNoiseDetection: false},
        {googAudioMirroring: false}
      ]
    },
    video:
    {
      mandatory: {
        chromeMediaSource: 'desktop',
        chromeMediaSourceId: source.id
      },
      optional: [
        {frameRate: {ideal: 60, min: 30}}
      ]
    }
  }

  const stream = await navigator.mediaDevices.getUserMedia(constraints);

  videoRoot.srcObject = stream;
  videoRoot.play();

  const options = { mimeType: 'video/webm; codecs=vp9' };
  mediaRecorder = new MediaRecorder(stream, options);

  mediaRecorder.ondataavailable = handleDataAvailable;
  mediaRecorder.onstop = handleStop;
}


function handleDataAvailable(event) {
  console.log('data available')
  recordedChunks.push(event.data);
}

async function handleStop(event) {
  const blob = new Blob(recordedChunks, {
    type: 'video/webm; codecs=vp9'
  });

  const buffer = Buffer.from(await blob.arrayBuffer());

  const { filePath } = await dialog.showSaveDialog({
    buttonLabel: 'Save video',
    defaultPath: `vid-${Date.now()}.webm`
  });

  console.log(filePath);

  writeFile(filePath, buffer, () => console.log('File written'));
}