val = 0;

function change(i)
{
    console.log(i);
    val = i;
}

function clickButton(id, sources) {
    console.log(id);
  document.getElementById(id).src=sources[val]; // Click on the checkbox
  document.getElementById(id).style.opacity = "1";
}