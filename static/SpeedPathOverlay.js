function SpeedPathOverlay(map, positions, bounds) {
    google.maps.OverlayView.call(this);
    this.positions_ = positions;
    this.map_ = map;
    this.bounds_ = bounds;
    this.setMap(map);
}

SpeedPathOverlay.prototype = new google.maps.OverlayView();

SpeedPathOverlay.prototype.onRemove = function() {
    if (this.canvas_) {
        this.canvas_.parentNode.removeChild(this.canvas_);
        this.canvas_ = null;
        this.ctx_ = null;
        this.positions_ = null;
        this.bounds_ = null;
    }
}

SpeedPathOverlay.prototype.onAdd = function() {
    canvas = document.createElement('CANVAS');
    canvas.style.position = 'absolute'
    canvas.style.padding = '0px';
    canvas.style.margin = '0px';
    this.canvas_ = canvas;
    var panes = this.getPanes();
    panes.overlayLayer.appendChild(canvas);

    if (!canvas.getContext) {
        alert("Need canvas!");
        return;
    }

    if (this.positions_.length < 2) {
        alert("Fewer than 2 positions");
        return;
    }
    this.ctx_ = canvas.getContext('2d');   
}

SpeedPathOverlay.prototype.draw = function() {
    var canvas = this.canvas_;
    var positions = this.positions_;
    var pts = positions.length;
    var proj = this.getProjection();
    var ctx = this.ctx_;
    var sw = proj.fromLatLngToDivPixel(this.bounds_.getSouthWest());
    var ne = proj.fromLatLngToDivPixel(this.bounds_.getNorthEast());
    var mb = this.map_.getBounds();
    // Resize the canvas to fit the indicated dimensions.
    var left = sw.x;
    var top = ne.y;
    canvas.style.left = left + 'px';
    canvas.style.top = top + 'px';
    canvas.setAttribute('width', ne.x - sw.x);
    canvas.setAttribute('height', sw.y - ne.y);

    //draw black outline
    ctx.linecap = 'round';
    ctx.lineWidth=7;
    ctx.strokeStyle = 'rgb(0,0,0)';
    ctx.beginPath();
    var j = 0;
    for (;j<pts;j++) {
        position = positions[j];
        position.point = proj.fromLatLngToDivPixel(position.latLong);
        position.point.x -= left;
        position.point.y -= top;

        if (j == 0) {
            ctx.moveTo(position.point.x, position.point.y);
        } else {
            ctx.lineTo(position.point.x, position.point.y);
        }
    }
    ctx.stroke();

    //then draw thinner, colorful lines
    ctx.lineWidth=5;

    var currentPoint = positions[0].point;
    var currentX = currentPoint.x;
    var currentY = currentPoint.y;
    var position;
    var j = 1;

    for (;j<pts;j++) {
        position = positions[j];
        if (position.color) {
            ctx.strokeStyle = "rgb(" + position.color[0] + "," + position.color[1] + "," + position.color[2] + ")";
        } else {
            var c = 25 * position.spd;
            ctx.strokeStyle = "rgb(" + c + "," + c + "," + c + ")";
        }
        ctx.beginPath();
        ctx.moveTo(currentX, currentY);
        currentPoint = position.point;
        currentX = currentPoint.x;
        currentY = currentPoint.y;
        ctx.lineTo(currentX, currentY);
        ctx.stroke();
    }
}