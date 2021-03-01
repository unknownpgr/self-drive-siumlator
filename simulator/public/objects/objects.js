/**
 * 이 파일은 시뮬레이션에 추가할 장애물을 설정하기 위한 파일입니다.
 * 장애물을 추가하려면,
 * 
 * 1. 먼저 장애물에 대한 .obj형식 파일을 objects 폴더에 집어넣습니다.
 * 2. 아래 objects 배열에 새로운 설정을 집어넣어줍니다.
 * 
 * filename은 말 그대로 파일의 이름입니다.
 * position은 위치입니다. 단위는 cm이며, x,y,z순서로 설정하면 됩니다.
 * 차량의 초기 위치를 기준으로, x방향은 앞쪽, y방향은 위쪽, z방향은 오른쪽입니다.
 * 
 * rotation은 말 그대로 회전입니다. x,y,z축을 기준으로 반시계방향으로 회전합니다. 
 * 
 * scale은 장애물의 x,y,z방향 크기입니다. 어떤 오브젝트의 경우, 시뮬레이션에 집어넣어보면 너무 작거나 큰 경우가 있습니다.
 * 이때 이 값을 적절히 조절하면 오브젝트를 적당히 줄일 수 있습니다.
 * 
 * color는 장애물의 색깔입니다. 포토샵이나 HTML에서 사용하는 16진수 표기법을 그대로 따릅니다.
 */

const objects = [
    {
        filename: 'human.obj',
        position: [250, 0, 0],
        color: '#404040',
    },
    {
        filename: 'laptop.obj',
        position: [249, 9, 0],
        scale: [0.2, 0.2, 0.2],
        rotation: [0, Math.PI, 0],
        color: '#ff4040',
    }
    /*
    {
        filename: 'some-new-object.obj',
        position: [249, 9, 100],
        scale: [0.2, 0.2, 0.2],
        rotation: [0, Math.PI, 0],
        color: '#404040',
    }
     */
];

export default objects;