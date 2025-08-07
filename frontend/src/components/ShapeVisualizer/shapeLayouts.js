
export const circleProps = {
    r: 20,
    fill: "#4e79a7",
};

export const layouts = {
    1: {
        points: [{ x: 250, y: 250 }],
        lines: []
    },
    2: {
        points: [
            { x: 50, y: 250 },
            { x: 450, y: 250 }
        ],
        lines: [[0, 1]]
    },
    3: {
        points: [
            { x: 250, y: 80 },
            { x: 50, y: 420 },
            { x: 450, y: 420 }
        ],
        lines: [[0, 1], [1, 2], [2, 0]]
    },
    4: {
        points: [
            { x: 50, y: 50 },
            { x: 450, y: 50 },
            { x: 50, y: 450 },
            { x: 450, y: 450 }
        ],
        lines: [[0, 1], [1, 3], [3, 2], [2, 0]]
    }
};