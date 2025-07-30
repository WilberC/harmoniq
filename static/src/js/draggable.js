function initializeDraggable() {
    let isDragging = false;
    let currentModal = null;
    let dragOffset = { x: 0, y: 0 };
    let originalPosition = { x: 0, y: 0 };
    let originalZIndex = 0;

    // Add drag handle to all modals
    function addDragHandles() {
        const modals = document.querySelectorAll('.modal');

        modals.forEach(modal => {
            // Check if modal already has drag handle
            if (modal.querySelector('.modal-drag-handle')) {
                return;
            }

            const header = modal.querySelector('.modal-header');
            if (header) {
                // Add cursor style to header to indicate it's draggable
                header.style.cursor = 'grab';
                header.classList.add('modal-drag-handle');

                // Add visual indicator for draggable area
                header.addEventListener('mouseenter', () => {
                    if (!isDragging) {
                        header.style.cursor = 'grab';
                    }
                });

                header.addEventListener('mouseleave', () => {
                    if (!isDragging) {
                        header.style.cursor = 'default';
                    }
                });
            }
        });
    }

    // Check if element is interactive (should not trigger drag)
    function isInteractiveElement(element) {
        const interactiveSelectors = [
            'button', 'input', 'select', 'textarea', 'a',
            '.btn', '.modal-close', '.window-control', '.tab',
            '[data-modal]', '[onclick]'
        ];

        return interactiveSelectors.some(selector =>
            element.matches(selector) || element.closest(selector)
        );
    }

    // Get modal position from transform
    function getModalPosition(modal) {
        const transform = window.getComputedStyle(modal).transform;
        const matrix = new DOMMatrix(transform);
        const rect = modal.getBoundingClientRect();

        // If modal is centered (default state), calculate center position
        if (matrix.m41 === 0 && matrix.m42 === 0) {
            return {
                x: (window.innerWidth - rect.width) / 2,
                y: (window.innerHeight - rect.height) / 2
            };
        }

        return {
            x: matrix.m41,
            y: matrix.m42
        };
    }

    // Set modal position
    function setModalPosition(modal, x, y) {
        // Remove the centered positioning and use absolute positioning
        modal.style.top = 'auto';
        modal.style.left = 'auto';
        modal.style.transform = `translate(${x}px, ${y}px)`;
    }

    // Constrain position to viewport
    function constrainToViewport(x, y, modal) {
        const rect = modal.getBoundingClientRect();
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;

        // Keep at least 50px of modal visible
        const minVisible = 50;

        let constrainedX = x;
        let constrainedY = y;

        // Constrain horizontally
        if (x + rect.width < minVisible) {
            constrainedX = minVisible - rect.width;
        } else if (x > viewportWidth - minVisible) {
            constrainedX = viewportWidth - minVisible;
        }

        // Constrain vertically
        if (y + rect.height < minVisible) {
            constrainedY = minVisible - rect.height;
        } else if (y > viewportHeight - minVisible) {
            constrainedY = viewportHeight - minVisible;
        }

        return { x: constrainedX, y: constrainedY };
    }

    // Start dragging
    function startDrag(event, modal) {
        if (isInteractiveElement(event.target)) {
            return;
        }

        event.preventDefault();
        isDragging = true;
        currentModal = modal;

        // Store original position and z-index
        const position = getModalPosition(modal);
        originalPosition = { ...position };
        originalZIndex = parseInt(window.getComputedStyle(modal).zIndex) || 100;

        // Calculate drag offset
        const rect = modal.getBoundingClientRect();
        dragOffset = {
            x: event.clientX - rect.left,
            y: event.clientY - rect.top
        };

        // Bring modal to front
        modal.style.zIndex = 1000;

        // Add dragging class for visual feedback
        modal.classList.add('dragging');

        // Change cursor
        const header = modal.querySelector('.modal-header');
        if (header) {
            header.style.cursor = 'grabbing';
        }

        // Add event listeners for drag and end
        document.addEventListener('mousemove', handleDrag);
        document.addEventListener('mouseup', stopDrag);

        // Prevent text selection during drag
        document.body.style.userSelect = 'none';
    }

    // Handle dragging
    function handleDrag(event) {
        if (!isDragging || !currentModal) return;

        event.preventDefault();

        // Calculate new position
        const newX = event.clientX - dragOffset.x;
        const newY = event.clientY - dragOffset.y;

        // Constrain to viewport
        const constrained = constrainToViewport(newX, newY, currentModal);

        // Apply position
        setModalPosition(currentModal, constrained.x, constrained.y);
    }

    // Stop dragging
    function stopDrag(event) {
        if (!isDragging || !currentModal) return;

        isDragging = false;

        // Remove dragging class
        currentModal.classList.remove('dragging');

        // Restore original z-index if modal is not active
        if (!currentModal.classList.contains('active')) {
            currentModal.style.zIndex = originalZIndex;
        }

        // Restore cursor
        const header = currentModal.querySelector('.modal-header');
        if (header) {
            header.style.cursor = 'grab';
        }

        // Remove event listeners
        document.removeEventListener('mousemove', handleDrag);
        document.removeEventListener('mouseup', stopDrag);

        // Restore text selection
        document.body.style.userSelect = '';

        currentModal = null;
    }

    // Reset modal to center position
    function resetModalToCenter(modal) {
        modal.style.top = '50%';
        modal.style.left = '50%';
        modal.style.transform = 'translate(-50%, -50%) scale(1)';
    }

    // Initialize drag functionality for a modal
    function initializeModalDrag(modal) {
        const header = modal.querySelector('.modal-header');
        if (!header) return;

        // Add mousedown event listener to header
        header.addEventListener('mousedown', (event) => {
            startDrag(event, modal);
        });

        // Prevent drag on interactive elements within header
        header.addEventListener('mousedown', (event) => {
            if (isInteractiveElement(event.target)) {
                event.stopPropagation();
            }
        }, true);

        // Reset modal to center when it becomes active (for newly opened modals)
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                    const isActive = modal.classList.contains('active');
                    const wasActive = mutation.oldValue && mutation.oldValue.includes('active');

                    // If modal just became active and wasn't positioned before, center it
                    if (isActive && !wasActive) {
                        const transform = window.getComputedStyle(modal).transform;
                        const matrix = new DOMMatrix(transform);

                        // Only center if it's in the default centered position
                        if (matrix.m41 === 0 && matrix.m42 === 0) {
                            resetModalToCenter(modal);
                        }
                    }
                }
            });
        });

        observer.observe(modal, {
            attributes: true,
            attributeOldValue: true
        });
    }

    // Initialize all existing modals
    function initializeExistingModals() {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            initializeModalDrag(modal);
        });
        addDragHandles();
    }

    // Watch for new modals (for dynamically added modals)
    function observeModalChanges() {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        // Check if the added node is a modal
                        if (node.classList && node.classList.contains('modal')) {
                            initializeModalDrag(node);
                        }
                        // Check if any modal was added within the node
                        const modals = node.querySelectorAll ? node.querySelectorAll('.modal') : [];
                        modals.forEach(modal => {
                            initializeModalDrag(modal);
                        });
                    }
                });
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // Handle window resize to keep modals in bounds
    function handleWindowResize() {
        const activeModals = document.querySelectorAll('.modal.active');
        activeModals.forEach(modal => {
            const position = getModalPosition(modal);
            const constrained = constrainToViewport(position.x, position.y, modal);
            setModalPosition(modal, constrained.x, constrained.y);
        });
    }

    // Initialize everything
    function init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                initializeExistingModals();
                observeModalChanges();
                window.addEventListener('resize', handleWindowResize);
            });
        } else {
            initializeExistingModals();
            observeModalChanges();
            window.addEventListener('resize', handleWindowResize);
        }
    }

    // Start initialization
    init();
}

export default initializeDraggable;
