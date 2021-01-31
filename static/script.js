var val = 0;
var x = 0;
var y = 0;
var data = [];
var sources = [];
var counters = [];
var labels = [];
var changes = [];
var rotation = 0;
var rotation_modes = []

function rotate()
{
    rotation = (rotation+90)%360;
}

function createData()
{
    for (i = 0; i < y; i++)
    {
        var l = [];
        var l_changes = [];
        for (j = 0; j < x; j++)
        {
            counters[0]++;
            l.push([0, counters[0], 0]);
            l_changes.push(true);
        }
        data.push(l);
        changes.push(l_changes);
    }
}

function createImage(act_val, rect)
{
    var img = document.createElement("img");
    img.src = sources[act_val]
    img.style.position = "absolute";
    img.style.width = "50px";
    img.style.height = "50px";
    //img.style.top = rect.top.toString()+"px";
    //img.style.left = rect.left.toString()+"px";

    return img;
}

function addDrawings(act_val, drawingsDiv, opacity, rect, rot, x1, y1)
{
    drawingsDiv.innerHTML = "";

    if (act_val == 1) {
        if (act_val == sources.length - 1)
            console.log(x1 + " " + y1);
        var count_legs = 0;
        if (y1 > 0) {
            var p = data[y1-1][x1];
            if (p[0] == 1 || p[0] == sources.length - 1 || (p[0] != 0 && (p[2] == 0 || p[2] == 180))) {
                var img = createImage(act_val, rect);
                img.style.opacity = opacity.toString();
                drawingsDiv.appendChild(img);
                count_legs++;
            }
        }
        if (y1 < y-1) {
            var p = data[y1+1][x1];
            if (p[0] == 1 || p[0] == sources.length - 1 || (p[0] != 0 && (p[2] == 0 || p[2] == 180))) {
                var img = createImage(act_val, rect);
                img.style.opacity = opacity.toString();
                img.style.transform = "rotate(180deg)";
                drawingsDiv.appendChild(img);
                count_legs++;
            }
        }
        if (x1 > 0) {
            var p = data[y1][x1-1];
            if (p[0] == 1 || p[0] == sources.length - 1 || (p[0] != 0 && (p[2] == 90 || p[2] == 270))) {
                var img = createImage(act_val, rect);
                img.style.opacity = opacity.toString();
                img.style.transform = "rotate(270deg)";
                drawingsDiv.appendChild(img);
                count_legs++;
            }
        }
        if (x1 < x-1) {
            var p = data[y1][x1+1];
            if (p[0] == 1 || p[0] == sources.length - 1 || (p[0] != 0 && (p[2] == 90 || p[2] == 270))) {
                var img = createImage(act_val, rect);
                img.style.opacity = opacity.toString();
                img.style.transform = "rotate(90deg)";
                drawingsDiv.appendChild(img);
                count_legs++;
            }
        }
        if (count_legs > 2) {
            var img = createImage(sources.length - 1, rect);
            img.style.opacity = opacity.toString();
            drawingsDiv.appendChild(img);
        }
    }
    else {
        var img = createImage(act_val, rect);
        img.style.opacity = opacity.toString();
        if (rotation_modes[act_val] == 2) {
            if (rot == 90 || rot == 270) {
                img.style.transform = "rotate(270deg)";
            }
        }
        else if (rotation_modes[act_val] == 1) {
            img.style.transform = "rotate("+rot+"deg)";
        }

        drawingsDiv.appendChild(img);
    }
}

function updateNumbers(x_pos, y_pos)
{
    act_val = data[y_pos][x_pos][0];
    count_val = data[y_pos][x_pos][1];
    counters[act_val]--;

    for (var i = 0; i < y; i++)
    {
        for (var j = 0; j < x; j++)
        {
            if (data[i][j][0] == act_val && data[i][j][1] > count_val)
            {
                data[i][j][1]--;
                changes[i][j] = true;
            }
        }
    }
}

function updateBoard()
{
    for (var i = 0; i<y; i++)
    {
        for (var j = 0; j<x; j++)
        {
            var act_val = data[i][j][0];
            if (!changes[i][j] && act_val != 1)
                continue;
            var id = i*100+j;
            id = id.toString();
            /*
            cell = document.getElementById("c"+id);
            cell.style.top = (150+i*50)+"px";
            cell.style.left = (200+j*50)+"px";
            */
            element = document.getElementById("i"+id);
            var rect = element.getBoundingClientRect();

            labelDiv = document.getElementById("l"+id);
            //labelDiv.style.top = rect.top.toString()+"px";
            //labelDiv.style.left = rect.left.toString()+"px";
            labelDiv.innerHTML = "";
            if (labels[act_val] != "")
            {
                labelDiv.innerHTML = "$"+labels[act_val]+"_"+data[i][j][1]+"$";
                MathJax.Hub.Queue(["Typeset",MathJax.Hub,labelDiv]);
            }

            drawingsDiv = document.getElementById("d"+id);
            //drawingsDiv.style.top = rect.top.toString()+"px";
            //drawingsDiv.style.left = rect.left.toString()+"px";

            addDrawings(act_val, drawingsDiv, 1, rect, data[i][j][2], j, i);

            changes[i][j] = false;
        }
    }
}

function clickButton(id)
{
    y_pos = Math.floor(id/100);
    x_pos = id%100;

    updateNumbers(x_pos, y_pos);

    counters[val]++;
    data[y_pos][x_pos][0] = val;
    data[y_pos][x_pos][1] = counters[val];
    data[y_pos][x_pos][2] = rotation;
    changes[y_pos][x_pos] = true;

    updateBoard();
}
function onMouse(id)
{
    drawingsDiv = document.getElementById("d"+id);
    var rect = drawingsDiv.getBoundingClientRect();
    addDrawings(val, drawingsDiv, 0.4, rect, rotation, id%100, Math.floor(id/100));
}
function offMouse(id)
{
    drawingsDiv = document.getElementById("d"+id);
    var rect = drawingsDiv.getBoundingClientRect();
    var componentData = data[Math.floor(id/100)][id%100]
    addDrawings(componentData[0], drawingsDiv, 1, rect, componentData[2], id%100, Math.floor(id/100));
}

function sendData()
{
    fetch("/", {
        method: "POST",
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
    })
}