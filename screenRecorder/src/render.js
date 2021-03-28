const videoRoot = document.getElementById('video__root');
const startButton = document.getElementById('start__button');
const stopButton = document.getElementById('stop__button');
const videoSelectButton = document.getElementById('video__select__button');

const { desktopCapturer, remote, dialog } = require('electron');
const { writeFile } = require('original-fs');
const { Menu } = remote;

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

let mediaRecorder;
const recordedChunks = [];

async function selectSource(source) {
  videoSelectButton.innerText = source.name;

  const constraints = {
    audio: false,
    video: {
      mandatory: {
        chromeMediaSource: 'desktop',
        chromeMediaSourceId: source.id
      }
    }
  }

  const stream = await navigator.mediaDevices.getUserMedia(constraints);

  videoRoot.srcObject = stream;
  videoRoot.play();

  const options = { mimeType: 'video/webm; codecs=vp9' };
  mediaRecorder = new MediaRecorder(stream, options);

  mediaRecorder.ondataavailable = handleDataAvailable
  mediaRecorder.onstop = handleStop;
}


function handleDataAvailable(event) {
  recordedChunks.push(event.data);
}

async function handleStop(event) {
  const blob = new Blob(recordedChunks, {
    type: 'video/webm: codecs=vp9'
  });

  const buffer = Buffer.from(await blob.arrayBuffer());

  const { filePath } = await dialog.showSaveDialog({
    buttonLabel: 'Save video',
    defaultPath: `vid-${Date.now()}.webm`
  });

  console.log(filePath)

  writeFile(filePath, buffer, () => console.log('File written'))
}

videoSelectButton.onclick = getVideoSources;