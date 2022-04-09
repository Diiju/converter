// This plugin will open a window to prompt the user to enter a number, and
// it will then create that many rectangles on the screen.

// This file holds the main code for the plugins. It has access to the *document*.
// You can access browser APIs in the <script> tag inside "ui.html" which has a
// full browser environment (see documentation).

// This shows the HTML page in "ui.html".
figma.showUI(__html__);

// Calls to "parent.postMessage" from within the HTML page will trigger this
// callback. The callback will be passed the "pluginMessage" property of the
// posted message.

var opendict = {};
var components = {};
var waiting = {};
var temp = "k";

function write_rang(data, images){
  temp = data;
  for (let i=0; i<data.length; i++){
    if (data[i]["type"] === "RGB"){
      temp[i]["type"] = "SOLID";
      if (data[i]["color"]){
        temp[i]["color"]["r"] = data[i]["color"]["r"]/255;
        temp[i]["color"]["g"] = data[i]["color"]["g"]/255;
        temp[i]["color"]["b"] = data[i]["color"]["b"]/255;
        if (data[i]["color"]["a"]){
          temp[i]["opacity"] = data[i]["color"]["a"];
          delete data[i]["color"]["a"];
        }
      }
    }

    if (data[i]["type"] === "HEX"){
      temp[i]["type"] = "SOLID"
      temp[i]["color"]["r"] = hexToRgb(data[i]["value"]).r;
      temp[i]["color"]["g"] = hexToRgb(data[i]["value"]).g;
      temp[i]["color"]["b"] = hexToRgb(data[i]["value"]).b;

      delete temp[i]["value"];
    }

    if (data[i]["type"] === "GRADIENT_LINEAR"){
      temp[i]["gradientHandlePositions"] = [[data[i]["x1"], data[i]["y1"]], [0, 0], [data[i]["x2"], data[i]["y2"]]];
      temp[i]["gradientStops"] = [];

      for (let j=0; i<data[i]["stops"].length; i++){
        temp[i]["gradientStops"][j]["position"] = data[i]["stops"][j]["pos"];
        if (data[i]["stops"][j]["rang"]){
          temp[i]["gradientStops"][j]["color"]["r"] = data[i]["stops"][j]["rang"]["r"]/255;
          temp[i]["gradientStops"][j]["color"]["g"] = data[i]["stops"][j]["rang"]["g"]/255;
          temp[i]["gradientStops"][j]["color"]["b"] = data[i]["stops"][j]["rang"]["b"]/255;
          if (data[i]["stops"][j]["rang"]["a"]){
            temp[i]["opacity"] = data[i]["stops"][j]["rang"]["a"];
            delete data[i]["stops"][j]["rang"]["a"];
          }
        }  
      }

      delete temp[i]["stops"];
      delete temp[i]["x1"];
      delete temp[i]["x2"];
      delete temp[i]["y1"];
      delete temp[i]["y2"];
    }

    if (data[i]["type"] === "GRADIENT_RADIAL"){
      temp[i]["gradientHandlePositions"] = [[data[i]["cx"], data[i]["cy"]], [data[i]["cx"] + data[i]["r1"], data[i]["cy"]], [data[i]["cx"], data[i]["cy"] - data[i]["r2"]]];
      temp[i]["gradientStops"] = [];

      for (let j=0; i<data[i]["stops"].length; i++){
        temp[i]["gradientStops"][j]["position"] = data[i]["stops"][j]["pos"];
        if (data[i]["stops"][j]["rang"]){
          temp[i]["gradientStops"][j]["color"]["r"] = data[i]["stops"][j]["rang"]["r"]/255;
          temp[i]["gradientStops"][j]["color"]["g"] = data[i]["stops"][j]["rang"]["g"]/255;
          temp[i]["gradientStops"][j]["color"]["b"] = data[i]["stops"][j]["rang"]["b"]/255;
          if (data[i]["stops"][j]["rang"]["a"]){
            temp[i]["opacity"] = data[i]["stops"][j]["rang"]["a"];
            delete data[i]["stops"][j]["rang"]["a"];
          }
        }  
      }

      delete temp[i]["stops"];
      delete temp[i]["cx"];
      delete temp[i]["cy"];
      delete temp[i]["r1"];
      delete temp[i]["r2"];
    }

    if (data[i]["type"] === "GRADIENT_ANGULAR"){
      var x3 = data[i]["x2"] - data[i]["x1"];
      var y3 = data[i]["y2"] - data[i]["y2"];
      var x_3 = (x3 * Math.cos(data[i]["rot"])) - (y3 * Math.sin(data[i]["rot"]));
      var y_3 = (y3 * Math.cos(data[i]["rot"])) + (x3 * Math.sin(data[i]["rot"]));
      x_3 = x_3 + data[i]["x1"];
      y_3 = y_3 + data[i]["y1"];
      temp[i]["gradientHandlePositions"] = [[data[i]["x1"], data[i]["y1"]], [data[i]["x2"], data[i]["y2"]], [x_3, y_3]];
      temp[i]["gradientStops"] = [];

      for (let j=0; i<data[i]["stops"].length; i++){
        temp[i]["gradientStops"][j]["position"] = data[i]["stops"][j]["pos"];
        if (data[i]["stops"][j]["rang"]){
          temp[i]["gradientStops"][j]["color"]["r"] = data[i]["stops"][j]["rang"]["r"]/255;
          temp[i]["gradientStops"][j]["color"]["g"] = data[i]["stops"][j]["rang"]["g"]/255;
          temp[i]["gradientStops"][j]["color"]["b"] = data[i]["stops"][j]["rang"]["b"]/255;
          if (data[i]["stops"][j]["rang"]["a"]){
            temp[i]["opacity"] = data[i]["stops"][j]["rang"]["a"];
            delete data[i]["stops"][j]["rang"]["a"];
          }
        }  
      }

      delete temp[i]["stops"];
      delete temp[i]["x1"];
      delete temp[i]["x2"];
      delete temp[i]["y1"];
      delete temp[i]["y2"];
      delete temp[i]["rot"];
    }

    if (data[i]["type"] === "GRADIENT_DAIMOND"){
      temp[i]["gradientHandlePositions"] = [[data[i]["cx"], data[i]["cy"]], [data[i]["cx"] + data[i]["r1"], data[i]["cy"]], [data[i]["cx"], data[i]["cy"] - data[i]["r2"]]];
      temp[i]["gradientStops"] = [];

      for (let j=0; i<data[i]["stops"].length; i++){
        temp[i]["gradientStops"][j]["position"] = data[i]["stops"][j]["pos"];
        if (data[i]["stops"][j]["rang"]){
          temp[i]["gradientStops"][j]["color"]["r"] = data[i]["stops"][j]["rang"]["r"]/255;
          temp[i]["gradientStops"][j]["color"]["g"] = data[i]["stops"][j]["rang"]["g"]/255;
          temp[i]["gradientStops"][j]["color"]["b"] = data[i]["stops"][j]["rang"]["b"]/255;
          if (data[i]["stops"][j]["rang"]["a"]){
            temp[i]["opacity"] = data[i]["stops"][j]["rang"]["a"];
            delete data[i]["stops"][j]["rang"]["a"];
          }
        }  
      }

      delete temp[i]["stops"];
      delete temp[i]["cx"];
      delete temp[i]["cy"];
      delete temp[i]["r1"];
      delete temp[i]["r2"];
    }        

    if (data[i]["type"] === "IMAGE"){
      //console.log(data["rang"][i]);
      let imageHash = figma.createImage(images[data[i]["id"]]).hash;
      temp[i]["imageHash"] = imageHash;

      delete temp[i]["id"];
    }
  }
  return temp;
}

function find_angle(x1, y1, x2, y2) {
  var AB = Math.sqrt(Math.pow(x2-x1,2)+ Math.pow(y2-y1,2));    
  var BC = Math.sqrt(Math.pow(x2-(x2+1),2)+ Math.pow(y2-y2,2)); 
  var AC = Math.sqrt(Math.pow((x2+1)-x1,2)+ Math.pow(y2-y1,2));
  return Math.acos((BC*BC+AB*AB-AC*AC)/(2*BC*AB))*180/Math.PI;
}

function find_length(x1,y1, x2, y2) {
  var length = (y2-y1);
  if (length<0){
      length = length*-1;
  }
  var width = (x2-x1);
  if (width<0){
      width = width*-1;
  }
  return {length, width};
}

function hexToRgb(hex) {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
}

//async function writer(data, par, sel, images)
async function writer(data, par, sel, images, string){
  if (data["type"] === "DOCUMENT") {
    element = figma.createPage();
    var t = data["bg_color"]["a"] 
    delete data["bg_color"]["a"]
    temp = {"type": "SOLID", "visible": true, "opacity": t, "color": data["bg_color"]}
    element.fills = temp;
    par.appendChild(element);
    for (let i=0; i<data["children"].length; i++){
      writer(data["children"][i], element, false, images, data["id"]);
    }
  }
  else {
    var element
    if (data["type"] === "block"){
      element = figma.createFrame();
      par.appendChild(element);
      if (sel){
        if (opendict[string]){
          opendict[string].push(element);
        }
        else{
          opendict[string] = [];
          opendict[string].push(element);
        }
      }
    }
    else if (data["type"] === "group"){
      if (data["children"]){
        if (data["isComponent"]){
          element = figma.createComponent();
          par.appendChild(element);
          components[data["id"]] = element;
          if(data["id"] in waiting){
            for(let i = 0; i < waiting[data["id"]].length; i++){
              writer(waiting[data["id"]][i][0], waiting[data["id"]][i][1], waiting[data["id"]][i][2], images, waiting[data["id"]][i][3]);
            }
            waiting[data["id"]] = [];
          }
        }
        else {
          for (let i=0; i<data["children"].length; i++){
            writer(data["children"][i], par, true, images, data["id"]);
          }
          if (data["isComponentSet"]){
            element = figma.combineAsVariants(opendict[data["id"]], par);  
            components[data["id"]] = element;
            if(data["id"] in waiting){
              for(let i = 0; i < waiting[data["id"]].length; i++){
                writer(waiting[data["id"]][i][0], waiting[data["id"]][i][1], waiting[data["id"]][i][2], images, waiting[data["id"]][i][3]);
              }
              waiting[data["id"]] = [];
            }
          }
          else {
            element = figma.group(opendict[data["id"]], par);
          }
          delete opendict[data["id"]];
        }
        if (sel){
          if (opendict[string]){
            opendict[string].push(element);
          }
          else{
            opendict[string] = [];
            opendict[string].push(element);
          }
        }
      }
    }
    else if (data["type"] === "vector"){
      element = figma.createVector();
      par.appendChild(element);
      if (sel){
        if (opendict[string]){
          opendict[string].push(element);
        }
        else{
          opendict[string] = [];
          opendict[string].push(element);
        }
      }
    }
    else if (data["type"] === "booleanOperation"){
      element = figma.createBooleanOperation();
      par.appendChild(element);
      if (sel){
        if (opendict[string]){
          opendict[string].push(element);
        }
        else{
          opendict[string] = [];
          opendict[string].push(element);
        }
      }
    }
    else if (data["type"] === "line"){
      element = figma.createLine();
      par.appendChild(element);
      if (sel){
        if (opendict[string]){
          opendict[string].push(element);
        }
        else{
          opendict[string] = [];
          opendict[string].push(element);
        }
      }
    }
    else if (data["type"] === "ellipse"){
      element = figma.createEllipse();
      par.appendChild(element);
      if (sel){
        if (opendict[string]){
          opendict[string].push(element);
        }
        else{
          opendict[string] = [];
          opendict[string].push(element);
        }
      }
    }
    else if (data["type"] === "polygon"){
      var element;
      if (data["starRatio"]){
        element = figma.createStar();
      }
      else {
        element = figma.createPolygon();
      }
      par.appendChild(element);
      if (sel){
        if (opendict[string]){
          opendict[string].push(element);
        }
        else{
          opendict[string] = [];
          opendict[string].push(element);
        }
      }
    }
    else if (data["type"] === "rect"){
      element = figma.createRectangle();
      par.appendChild(element);
      if (sel){
        if (opendict[string]){
          opendict[string].push(element);
        }
        else{
          opendict[string] = [];
          opendict[string].push(element);
        }
      }
    }
    else if (data["type"] === "text"){
      element = figma.createText();
      par.appendChild(element);
      if (sel){
        if (opendict[string]){
          opendict[string].push(element);
        }
        else{
          opendict[string] = [];
          opendict[string].push(element);
        }
      }
    }
    else if (data["type"] === "instance"){
      if(data["componentID"] in components){
        element = components[data["componentID"]].createInstance();
        par.appendChild(element);
      }
      else{
        if(data["componentID"] in waiting){
          waiting[data["componentID"]].push([data, par, sel, string]);
        }
        else{
          waiting[data["componentID"]] = [];
          waiting[data["componentID"]].push([data, par, sel, string]);
          return;
        }
      }
    }


    if (data["name"]){
      element.name = data["name"];
    }
    if (data["visibilty"]){
      element.visible = data["visible"];
    }
    if (data["locked"]){
      element.locked = data["locked"];
    }
    if (data["opacity"]){
      element.opacity = data["opacity"];
    }
    
    if (data["rang"]){
      element.fills = write_rang(data["rang"], images);
    }

    if (data["strokeParams"]){
      if (data["strokeParams"]["strokes"]){
        element.strokes = write_rang(data["strokeParams"]["strokes"], images);
      }
  
      if (data["strokeParams"]["strokeWeight"]){
        element.strokeWeight = data["strokeParams"]["strokeWeight"];
      }
      if (data["strokeParams"]["strokeAlign"]){
        temp = data["strokeParams"]["strokeAlign"];
        if (temp === "Inside"){
          temp = "INSIDE";
        }
        if (temp === "Outside"){
          temp = "OUTSIDE";
        }
        if (temp === "Center"){
          temp = "CENTER";
        }
        element.strokeAlign = temp;
      }
      if (data["strokeParams"]["strokeCap"]){
        temp = data["strokeParams"]["strokeCap"];
        temp = temp.toUpperCase();
        element.strokeCap = temp;
      }
      if (data["strokeParams"]["strokeJoin"]){
        element.strokeJoin = data["strokeParams"]["strokeJoin"].toUpperCase();
      }
      if (data["strokeParams"]["strokeDash"]){
        element.strokeDashes = data["strokeParams"]["strokeDashes"];
      }
      if (data["strokeParams"]["strokeMiter"]){
        element.strokeMiterAngle = data["strokeParams"]["strokeMiter"];
      }
      /*
      if (data["strokeParams"]["strokeGeometery"]){
        element.strokeGeometery = data["strokeParams"]["strokeGeometeryt"];
      }
      */
    }
    

    if (data["cornerRadius"]) {
      element.cornerRadius = data["cornerRadius"][0];
    }

    if (data["effects"]){
      temp = data["effects"];
      for (let i=0; i<data["effects"].length; i++){
        if (data["effects"][i]["type"] === "shadow"){
          if (data["effects"][i]["inner"] === true){
            temp[i]["type"] = "INNER_SHADOW";
            temp[i]["offset"] = [data["effects"][i]["X"], data["effects"][i]["Y"]];
            temp[i]["radius"] = data["effects"][i]["r"];
            temp[i]["color"] = {};
            temp[i]["color"]["r"] = data["effects"][i]["rang"]["r"]/255;
            temp[i]["color"]["g"] = data["effects"][i]["rang"]["g"]/255;
            temp[i]["color"]["b"] = data["effects"][i]["rang"]["b"]/255;
            temp[i]["color"]["a"] = data["effects"][i]["rang"]["a"];
          }
          else {
            temp[i]["type"] = "DROP_SHADOW";
            temp[i]["offset"] = [data["effects"][i]["X"], data["effects"][i]["Y"]];
            temp[i]["radius"] = data["effects"][i]["r"];
            temp[i]["color"] = write_rang(data["effects"][i]["rang"], images);
          }
        }
        else if (data["effects"][i]["type"] === "blur"){
          if (data["effects"][i]["background"] === true){
            temp[i]["type"] = "BACKGROUND_BLUR";
            temp[i]["radius"] = data["effects"][i]["amount"];
          }
          else {
            temp[i]["type"] = "LAYER_BLUR";
            temp[i]["radius"] = data["effects"][i]["amount"];
          }
        }
      }
      element.effects = temp;
    }

    if (data["X"]){
      element.x = data["X"];
    }

    if (data["Y"]){
      element.y = data["Y"];
    }

    if (data["rotation"]){
      element.rotation = data["rotation"];
    }
    
    if (data["width"]){
      element.resize(data["width"], data["height"]);
    }

    //preserve ratio not found

    if (data["blendMode"]){
      element.blendMode = data["blendMode"];
    }

    if (data["constraints"]) {
      element.constraints = data["constraints"]["normal"];
    }

    if (data["isMask"]){
      element.isMask = data["isMask"];
    }

    if (data["children"] && data["type"] != "group"){
      for (let i=0; i<data["children"].length; i++){
        // console.log(data["children"][i])
        writer(data["children"][i], element, false, images, data["id"]);
      }
    }

    if (data["type"] === "text"){
      if(data["styles"]){
        var start = 0;
        for (let i=0; i<data["styles"].length; i++){
          var l = data["styles"][i]["length"];
          if (data["styles"][i]["family"]){
            await figma.loadFontAsync({family: data["styles"][i]["family"], style: data["styles"][i]["style"]});
            //element.fontName = {family: data["styles"][i]["family"], style: data["styles"][i]["style"]};
            element.setRangeFontName(start, start+l, data["styles"][i]["family"]);
            element.characters = data["data"];        
          }
          if (data["styles"][i]["paragraphSpacing"]){
            element.paragraphSpacing = data["paragraphSpacing"];
          }
          if (data["styles"][i]["paragraphIndent"]){
            element.paragraphIndent = data["paragraphIndent"];
            //element.setRangeIndentation(start, start+l, data["styles"][i]["paragraphIndent"])
          }
          if (data["styles"][i]["size"]){
            //element.fontSize = data["styles"][i]["size"];
            element.setRangeFontSize(start, start+l, data["styles"][i]["size"]);
          }
          if (data["styles"][i]["textTransform"]){
            //element.textCase = data["styles"][i]["textTransform"];
            element.setRangeTextCase(start, start+l, data["styles"][i]["textTransform"]);
          }
          if (data["styles"][i]["underline"]){
            //element.textDecoration = "UNDERLINE";
            element.setRangeTextDecoration(start, start+l, "UNDERLINE");
          }
          if (data["styles"][i]["srikethrough"]){
            //element.textDecoration = "STRIKETHROUGH";
            element.setRangeTextDecoration(start, start+l, "STRIKETHROUGH");
          }
          if (data["styles"][i]["textAlignHorizontal"]){
            element.textAlignHorizontal = data["textAllignHorizontal"];
          }
          /*
          if (data["styles"][i]["textAlignVertical"]){
            element.textAlignVertical= data["styles"][i]["textAlignVertical"];
          }*/
          if (data["styles"][i]["letterSpacing"]){
            //element.letterSpacing = data["styles"][i]["letterSpacing"];
            element.setRangeLetterSpacing(start, start+l, data["styles"][i]["letterSpacing"]);
          }
          if (data["styles"][i]["hyperlink"]){
            //element.hyperlink = data["styles"][i]["hyperlink"];
            element.setRangeHyperlink(start, start+l, data["styles"][i]["hyperlink"])
          }
          if (data["styles"][i]["rang"]){
            element.setRangeFills(start, start+l, write_rang(data["styles"][i]["rang"], images));
          }
        }
      }
      if (data["textType"]){
        if (data["textType"] === "area"){
          element.textAutoResize = "NONE";
        }
        else if (data["textType"] === "autoHeight"){
          element.textAutoResize = "HEIGHT";
        }
        else if (data["textType"] === "point"){
          element.textAutoResize = "WIDTH_AND_HEIGHT";
        }
      }
      if (data["lineHeight"]){
        element.lineHeight = data["lineHeight"];
      }
    }

    if (data["type"] === "vector"){
      if (data["path"]){
        var temp;
        temp = [{"windingRule": data["windingRule"], "data": data["path"]}]
        element.vectorPaths = temp;
      }
    }

    if (data["type"] === "line"){
      element.rotation = find_angle(data["x1"], data["y1"], data["x2"], data["y2"]);
      element.resize(find_length(data["x1"], data["y1"], data["x2"], data["y2"]), 0);
    }

    if (data["type"] === "polygon"){
      element.pointCount = data["cornerCount"];
      if (data["startRatio"]) {
        element.innerRadius = data["starRatio"]/100;
      }
    }

    if (data["type"] == "ellipse"){
      element.resize(data["radiusX"] * 2, data["radiusY"] * 2);
    }

    if (data["type"] == "booleanOperation"){
      element.booleanOperation = data["op"];
    }

    if (data["type"] == "instance"){
      element.mainComponent = data["componentID"];
    }

  }
}

//figma.ui.onmessage = async msg
figma.ui.onmessage = async msg => {
  // One way of distinguishing between different types of messages sent from
  // your HTML page is to use an object with a "type" property like this.

  if(msg.type === 'send-data'){
    var data = msg.data.dj;
    var images = msg.data.ass;
    //await writer(data, figma.root, false, images);
    await writer(data, figma.root, false, images, "base");
  }

  if (msg.type === 'create-rectangles') {
    const nodes: SceneNode[] = [];
    for (let i = 0; i < msg.count; i++) {
      const rect = figma.createRectangle();
      rect.x = i * 150;
      rect.fills = [{type: 'SOLID', color: {r: 1, g: 0.5, b: 0}}];
      figma.currentPage.appendChild(rect);
      nodes.push(rect);
    }
    figma.currentPage.selection = nodes;
    figma.viewport.scrollAndZoomIntoView(nodes);
  }

  // Make sure to close the plugin when you're done. Otherwise the plugin will
  // keep running, which shows the cancel button at the bottom of the screen.
  figma.closePlugin();
};
