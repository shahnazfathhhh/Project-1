const videoElement = document.getElementById("video");
const canvasElement = document.getElementById("canvas");
const canvasCtx = canvasElement.getContext("2d");

const fingerText = document.getElementById("count");

function countFingers(landmarks){

let tips = [4,8,12,16,20];
let count = 0;

for(let i=1;i<tips.length;i++){

if(landmarks[tips[i]].y < landmarks[tips[i]-2].y){
count++;
}

}

return count;
}

function onResults(results){

canvasCtx.save();
canvasCtx.clearRect(0,0,canvasElement.width,canvasElement.height);

canvasCtx.drawImage(
results.image,
0,
0,
canvasElement.width,
canvasElement.height
);

if(results.multiHandLandmarks){

for(const landmarks of results.multiHandLandmarks){

let fingers = countFingers(landmarks);

fingerText.innerText = "Fingers: " + fingers;

for(let i=0;i<landmarks.length;i++){

let x = landmarks[i].x * canvasElement.width;
let y = landmarks[i].y * canvasElement.height;

canvasCtx.beginPath();
canvasCtx.arc(x,y,5,0,2*Math.PI);
canvasCtx.fillStyle="red";
canvasCtx.fill();
}

}

}

canvasCtx.restore();
}

const hands = new Hands({

locateFile:(file)=>{
return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
}

});

hands.setOptions({

maxNumHands:1,
modelComplexity:1,
minDetectionConfidence:0.7,
minTrackingConfidence:0.7

});

hands.onResults(onResults);

const camera = new Camera(videoElement,{
onFrame: async()=>{
await hands.send({image:videoElement});
},
width:640,
height:480
});

camera.start();