var val = 0;
var x = 0;
var y = 0;
var data = [];
var sources = [];
var counters = [];
var labels = [];
var changes = [];
var rotation = [];

function createData()
{
    for (i = 0; i < y; i++)
    {
        var l = [];
        var l_changes = [];
        for (j = 0; j < x; j++)
        {
            counters[0]++;
            l.push([0, counters[0]]);
            l_changes.push(true);
        }
        data.push(l);
        changes.push(l_changes);
    }
}

function addDrawings(act_val, drawingsDiv, opacity, rect)
{
    drawingsDiv.innerHTML = "";

    var img = document.createElement("img");
    img.src = sources[act_val]
    img.class = "abs_img";
    img.style.top = rect.top.toString()+"px";
    img.style.left = rect.left.toString()+"px";
    img.style.opacity = opacity.toString();
    drawingsDiv.appendChild(img);
}

function updateBoard()
{
    for (i = 0; i<y; i++)
    {
        for (j = 0; j<x; j++)
        {
            if (!changes[i][j])
                continue;
            changes[i][j] = false;
            var id = i*100+j;
            id = id.toString();
            var act_val = data[i][j][0];

            element = document.getElementById("i"+id);
            var rect = element.getBoundingClientRect();

            labelDiv = document.getElementById("l"+id);
            labelDiv.style.top = rect.top.toString()+"px";
            labelDiv.style.left = rect.left.toString()+"px";
            labelDiv.innerHTML = "";
            if (labels[act_val] != "")
            {
                labelDiv.innerHTML = "$"+labels[act_val]+"_"+data[i][j][1]+"$"
                MathJax.Hub.Queue(["Typeset",MathJax.Hub,labelDiv]);
            }

            drawingsDiv = document.getElementById("d"+id);
            drawingsDiv.style.top = rect.top.toString()+"px";
            drawingsDiv.style.left = rect.left.toString()+"px";

            addDrawings(act_val, drawingsDiv, 1, rect);
        }
    }
}

function clickButton(id)
{
    y_pos = Math.floor(id/100);
    x_pos = id%100;

    act_val = data[y_pos][x_pos][0];
    count_val = data[y_pos][x_pos][1];
    counters[act_val]--;

    for (i = 0; i < y; i++)
    {
        for (j = 0; j < x; j++)
        {
            if (data[i][j][0] == act_val && data[i][j][1] > count_val)
            {
                data[i][j][1]--;
                changes[i][j] = true;
            }
        }
    }

    counters[val]++;
    data[y_pos][x_pos][0] = val;
    data[y_pos][x_pos][1] = counters[val];
    changes[y_pos][x_pos] = true;

    updateBoard();
}
function onMouse(id)
{
    drawingsDiv = document.getElementById("d"+id);
    var rect = drawingsDiv.getBoundingClientRect();
    addDrawings(val, drawingsDiv, 0.4, rect);
}
function offMouse(id)
{
    drawingsDiv = document.getElementById("d"+id);
    var rect = drawingsDiv.getBoundingClientRect();
    addDrawings(data[Math.floor(id/100)][id%100][0], drawingsDiv, 1, rect);
}