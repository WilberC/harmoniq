# Draggable Modal System

This document describes the draggable modal functionality implemented in Harmoniq to simulate macOS window behavior.

## Features

### 🎯 Core Functionality
- **Drag by Header**: All modals can be dragged by clicking and holding on the modal header
- **Multi-Modal Support**: Multiple modals can be opened and dragged independently
- **Z-Index Management**: Dragged modals automatically come to the front
- **Boundary Constraints**: Modals are prevented from being dragged completely off-screen
- **Interactive Element Protection**: Buttons, inputs, and other interactive elements don't trigger dragging

### 🎨 Visual Feedback
- **Cursor Changes**: Header shows grab/grabbing cursor to indicate draggable area
- **Enhanced Shadow**: Dragged modals get a deeper shadow for visual feedback
- **Smooth Transitions**: Non-dragging state maintains smooth animations

### 🔧 Technical Features
- **Viewport Constraints**: Modals stay within viewport bounds with 50px minimum visibility
- **Window Resize Handling**: Modals reposition automatically when window is resized
- **Dynamic Modal Support**: New modals added to the DOM are automatically made draggable
- **Position Persistence**: Modal positions are maintained during drag operations

## Implementation Details

### Files Modified
- `static/src/js/draggable.js` - Main draggable functionality
- `static/src/js/desktop.js` - Integration with existing modal system
- `static/src/index.css` - CSS styles for draggable behavior

### Key Functions

#### `initializeDraggable()`
Main initialization function that sets up the draggable system.

#### `startDrag(event, modal)`
Handles the beginning of a drag operation:
- Prevents dragging on interactive elements
- Calculates drag offset
- Brings modal to front
- Adds visual feedback

#### `handleDrag(event)`
Manages the drag operation:
- Calculates new position
- Applies viewport constraints
- Updates modal position

#### `stopDrag(event)`
Completes the drag operation:
- Restores original z-index if needed
- Removes visual feedback
- Cleans up event listeners

#### `constrainToViewport(x, y, modal)`
Ensures modals stay within viewport bounds with minimum visibility.

## Usage

### For Users
1. **Open a Modal**: Click on any dock icon or modal trigger
2. **Drag Modal**: Click and hold on the modal header (title bar area)
3. **Move Around**: Drag the modal to any position on screen
4. **Multiple Modals**: Open multiple modals and drag them independently
5. **Close Modal**: Use the close button, escape key, or click outside

### For Developers
The draggable system is automatically initialized when the page loads. No additional setup is required.

```javascript
// The system is automatically initialized in desktop.js
import initializeDraggable from './draggable.js';
initializeDraggable();
```

## Browser Compatibility

- ✅ Chrome/Chromium (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge

## Testing

A test file `test-draggable.html` is provided to verify the functionality:

1. Start a local server: `python -m http.server 8080`
2. Open `http://localhost:8080/test-draggable.html`
3. Test opening multiple modals and dragging them around

## Customization

### CSS Customization
The draggable behavior can be customized by modifying the CSS classes:

```css
.modal-drag-handle {
    cursor: grab;
}

.modal.dragging {
    transition: none;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}
```

### JavaScript Customization
The draggable system can be extended by modifying the `draggable.js` file:

- Adjust viewport constraints in `constrainToViewport()`
- Modify drag sensitivity in `handleDrag()`
- Add custom visual feedback in `startDrag()` and `stopDrag()`

## Troubleshooting

### Common Issues

1. **Modal not draggable**: Ensure the modal has a `.modal-header` element
2. **Dragging interferes with buttons**: Interactive elements are automatically protected
3. **Modal disappears off-screen**: Viewport constraints should prevent this
4. **Z-index issues**: Dragged modals automatically come to front

### Debug Mode
Enable console logging by adding this to the browser console:
```javascript
localStorage.setItem('debugDraggable', 'true');
```

## Future Enhancements

Potential improvements for future versions:
- [ ] Snap-to-grid functionality
- [ ] Modal stacking order management
- [ ] Drag handles on different parts of modal
- [ ] Touch support for mobile devices
- [ ] Animation easing during drag operations
- [ ] Modal position persistence across sessions
