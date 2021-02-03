var val = 0;
var x = 0;
var y = 0;
var data = [];
var sources = [];
var counters = [];
var labels = [];
var changes = [];
var rotation = 0;
var rotation_modes = [];
var divContent = [];
var Cs = [];
var Ls = [];
var Es = [];
var Is = [];
var Rs = [];
var clicked = false;
var state = 0;

function changeVal(value)
{
    if (clicked)
        return;
    val = value;
}

function rotate()
{
    rotation = (rotation+90)%360;
    console.log(rotation);
}

function getInput()
{
    console.log(val);
    var first_val = parseFloat(document.getElementById('input1').value);
    var deg_val = parseFloat(document.getElementById('input2').value);
    var omega_val = parseFloat(document.getElementById('input3').value);

    if (labels[val] == "R") {
        Rs.push(first_val);
    }
    else if (labels[val] == "C") {
        Cs.push(first_val);
    }
    else if (labels[val] == "L") {
        Ls.push(first_val);
    }
    else if (labels[val] == "E") {
        Es.push([first_val, deg_val, omega_val]);
    }
    else if (labels[val] == "I") {
        Is.push([first_val, deg_val, omega_val]);
    }

    var acceptButton = document.getElementById('accept');
    acceptButton.disabled = true;
    clicked = false;
}

function createData()
{
    for (i = 0; i < y; i++)
    {
        var l = [];
        var l_changes = [];
        var l_drawings = [];
        for (j = 0; j < x; j++)
        {
            l_drawings.push(document.getElementById("d"+(i*100+j)).innerHTML);
            counters[0]++;
            l.push([0, counters[0], 0]);
            l_changes.push(true);
        }
        divContent.push(l_drawings);
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
            if (p[0] == 1 || labels[p[0]] == "S" || p[0] == sources.length - 1 ||
               (p[0] != 0 && (p[2] == 0 || p[2] == 180))) {
                var img = createImage(act_val, rect);
                img.style.opacity = opacity.toString();
                drawingsDiv.appendChild(img);
                count_legs++;
            }
        }
        if (y1 < y-1) {
            var p = data[y1+1][x1];
            if (p[0] == 1 || labels[p[0]] == "S" || p[0] == sources.length - 1 ||
               (p[0] != 0 && (p[2] == 0 || p[2] == 180))) {
                var img = createImage(act_val, rect);
                img.style.opacity = opacity.toString();
                img.style.transform = "rotate(180deg)";
                drawingsDiv.appendChild(img);
                count_legs++;
            }
        }
        if (x1 > 0) {
            var p = data[y1][x1-1];
            if (p[0] == 1 || labels[p[0]] == "S"|| p[0] == sources.length - 1 ||
               (p[0] != 0 && (p[2] == 90 || p[2] == 270))) {
                var img = createImage(act_val, rect);
                img.style.opacity = opacity.toString();
                img.style.transform = "rotate(270deg)";
                drawingsDiv.appendChild(img);
                count_legs++;
            }
        }
        if (x1 < x-1) {
            var p = data[y1][x1+1];
            if (p[0] == 1 || labels[p[0]] == "S" || p[0] == sources.length - 1 ||
               (p[0] != 0 && (p[2] == 90 || p[2] == 270))) {
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
            if (opacity == 1)
                data[y1][x1][2] = 360;
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
    console.log(labels[act_val]);
    if ("LCREI".includes(labels[act_val]) && labels[val] != "") {
        console.log(labels[act_val]);
        if (labels[act_val] == "R") {
            Rs.splice(count_val, 1);
        }
        else if (labels[act_val] == "C") {
            Cs.splice(count_val, 1);
        }
        else if (labels[act_val] == "L") {
            Ls.splice(count_val, 1);
        }
        else if (labels[act_val] == "E") {
            Es.splice(count_val, 1);
        }
        else if (labels[act_val] == "I") {
            Is.splice(count_val, 1);
        }
        console.log(Cs);
    }

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

            if (changes[i][j]) {
                var act_val = data[i][j][0];
                var id = i*100+j;
                id = id.toString();
                /*
                cell = document.getElementById("c"+id);
                cell.style.top = (150+i*50)+"px";
                cell.style.left = (200+j*50)+"px";
                */
                element = document.getElementById("i"+id);
                var rect = element.getBoundingClientRect();

                var labelDiv = document.getElementById("l"+id);
                //labelDiv.style.top = rect.top.toString()+"px";
                //labelDiv.style.left = rect.left.toString()+"px";
                labelDiv.innerHTML = "";
                if (labels[act_val] != "")
                {
                    labelDiv.innerHTML = "$"+labels[act_val]+"_"+(data[i][j][1]+1)+"$";
                    MathJax.Hub.Queue(["Typeset",MathJax.Hub,labelDiv]);
                }

                var drawingsDiv = document.getElementById("d"+id);
                //drawingsDiv.style.top = rect.top.toString()+"px";
                //drawingsDiv.style.left = rect.left.toString()+"px";

                addDrawings(act_val, drawingsDiv, 1, rect, data[i][j][2], j, i);
                divContent[i][j] = drawingsDiv.innerHTML;

                changes[i][j] = false;
            }
        }
    }
}

function clickButton(id)
{
    if (clicked)
        return;
    y_pos = Math.floor(id/100);
    x_pos = id%100;

    updateNumbers(x_pos, y_pos);

    data[y_pos][x_pos][0] = val;
    data[y_pos][x_pos][1] = counters[val];
    data[y_pos][x_pos][2] = rotation;
    counters[val]++;
    changes[y_pos][x_pos] = true;

    if ("LCREI".includes(labels[val]) && labels[val] != "") {
        clicked = true;
        var acceptButton = document.getElementById('accept');
        acceptButton.disabled = false;

        var dataLabel = document.getElementById('first_label');
        dataLabel.innerHTML = "$"+labels[val]+"_{"+counters[val]+"}$";
        MathJax.Hub.Queue(["Typeset",MathJax.Hub,dataLabel]);
    }

    if (y_pos > 0)
        changes[y_pos-1][x_pos] = true;
    if (y_pos < y-1)
        changes[y_pos+1][x_pos] = true;
    if (x_pos > 0)
        changes[y_pos][x_pos-1] = true;
    if (x_pos < x-1)
        changes[y_pos][x_pos+1] = true;

    updateBoard();
}
function onMouse(id)
{
    if (clicked)
        return;
    drawingsDiv = document.getElementById("d"+id);
    var rect = drawingsDiv.getBoundingClientRect();
    addDrawings(val, drawingsDiv, 0.4, rect, rotation, id%100, Math.floor(id/100));
}
function offMouse(id)
{
    if (clicked)
        return;
    drawingsDiv = document.getElementById("d"+id);
    drawingsDiv.innerHTML = divContent[Math.floor(id/100)][id%100];
    //var rect = drawingsDiv.getBoundingClientRect();
    //var componentData = data[Math.floor(id/100)][id%100]
    //addDrawings(componentData[0], drawingsDiv, 1, rect, componentData[2], id%100, Math.floor(id/100));
}

function displayEquations(equations, solvedEquations, solvedFor, result, time_equations, initial_conditions, variables_latex, passing, a, methods)
{
    console.log(a);
    if (a <= 1) {
        var display_string = "Initial Equations <br>";
        for (var i = 0; i < equations.length; i++) {
            display_string += "$"+equations[i]+"=0$<br>";
        }
        display_string += "<br><br>Solved Equations <br>";

        for (var i = 0; i < solvedEquations.length; i++) {
            display_string += "$"+solvedFor[i]+"="+solvedEquations[i]+"="+result[i]+"$<br>";
        }

        display_string += "<br><br>Time Conditions<br>";
        display_string += "$\\Bbb{x}";
        if (a == 1)
            display_string += "_{u}";
        display_string += "(t)=\\begin{bmatrix}";
        for (var i in variables_latex) {
            display_string += variables_latex[i]+"(t)\\\\ ";
        }
        display_string += "\\end{bmatrix}="+time_equations+"$<br>";
        display_string += "$\\Bbb{x}";
        if (a == 1)
            display_string += "_u(0^+)";
        else
            display_string += "(0^-)";
        display_string += "=\\begin{bmatrix}";
        for (var i in variables_latex) {
            display_string += variables_latex[i];
            if (a == 1)
                display_string += "(0^+)";
            else
                display_string += "(0^-)";
            display_string += "\\\\ ";
        }
        display_string += "\\end{bmatrix}="+initial_conditions+"$<br><br><br>";
        if (a == 1) {
            display_string += "Warunki przejściowe początkowe<br>";
            display_string += "$\\Bbb{x}_p(0^+)=\\begin{bmatrix}";
            for (var i in variables_latex) {
                display_string += variables_latex[i]+"(0^+)\\\\ ";
            }
            display_string += "\\end{bmatrix}="+passing+"$<br><br><br>";
        }

        var equationsElement = document.getElementById('equations');
        if (a == 1)
            equationsElement = document.getElementById('equations2');
        equationsElement.innerHTML = display_string;

        MathJax.Hub.Queue(["Typeset",MathJax.Hub,equationsElement]);
    }
    else if (a==2) {
        var display_string = "Initial Equations <br>";
        for (var i = 0; i < equations.length; i++) {
            display_string += "$"+equations[i]+"=0$<br>";
        }
        display_string += "<br><br>Solved Equations <br>";

        for (var i = 0; i < solvedEquations.length; i++) {
            display_string += "$"+solvedFor[i]+"="+solvedEquations[i]+"="+result[i]+"$<br>";
        }
        display_string += "<br><br>"+methods;
        var equationsElement = document.getElementById('equations3');
        equationsElement.innerHTML = display_string;

        MathJax.Hub.Queue(["Typeset",MathJax.Hub,equationsElement]);
    }
}

function addCurrents(intersections, pointCurrents, newGrid)
{
    for (var i = 0; i<y; i++) {
        for (var j = 0; j<x; j++) {
            changes[i][j] = true;
        }
    }
    updateBoard();
    var i = 0;
    for (var id in intersections)
    {
        var label = "P"+newGrid[Math.floor(id/100)][id%100][1];
        i++;
        var drawingsDiv = document.getElementById("d"+id);
        var labelDiv = document.getElementById("l"+id);
        labelDiv.innerHTML = "";

        for (var j = 0; j < 4; j++) {
            if (intersections[id][j] != "") {
                var img = document.createElement("img");
                console.log(pointCurrents);
                console.log(intersections[id][j]);
                console.log(label);
                if (pointCurrents[label][intersections[id][j]][1] == label) {
                    img.src = '/static/images/out_flow.svg';
                }
                else {
                    img.src = '/static/images/in_flow.svg';
                }
                img.style.position = "absolute";
                img.style.width = "50px";
                img.style.height = "50px";
                img.style.transform = "rotate("+j*90+"deg)";
                drawingsDiv.appendChild(img);

                var newLabel = document.createElement("div");
                newLabel.innerHTML = "$i_{"+(pointCurrents[label][intersections[id][j]][0]+1)+"}$";
                newLabel.style.position = "absolute";
                newLabel.style.width = "25px";
                newLabel.style.height = "25px";
                var hOptions = ["center", "right", "center", "left"];
                newLabel.style.textAlign = hOptions[j];
                var tOptions = ["0px", "25px", "30px", "5px"];
                var lOptions = ["25px", "25px", "0px", "0px"];
                newLabel.style.left = lOptions[j];
                newLabel.style.top = tOptions[j];
                labelDiv.appendChild(newLabel);
            }
        }
        divContent[Math.floor(id/100)][id%100] = drawingsDiv.innerHTML;
    }
    MathJax.Hub.Queue(["Typeset",MathJax.Hub,document.getElementById("content")]);
}

function sendData()
{
    state = (state + 1)%4;
    var prev = state - 1;
    if (prev < 0)
        prev = 2;
    fetch("/", {
        method: "POST",
        body: JSON.stringify([data, [Rs, Ls, Cs, Es, Is], prev])
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      displayEquations(data[2], data[4], data[5], data[6], data[7], data[8], data[9], data[10], prev, data[11]);
      addCurrents(data[0], data[1], data[3]);
    });

}