// Select the <source> element using its attribute
const sourceElement = document.querySelector('source[media="(prefers-color-scheme: dark)"]');

// Check if the element is found
if (sourceElement) {
    // Update the media attribute
    sourceElement.media = '(prefers-color-scheme: white)';
} else {
    console.error('Element not found');
}

// Select the <img> element
const imgElement = document.querySelector('img');

// Check if the element is found
if (imgElement) {
    // Change the width and height of the image
    imgElement.style.width = '200px'; // Set the width to 200 pixels
    imgElement.style.height = 'auto'; // Set the height to 150 pixels
} else {
    console.error('Image element not found');
}

// Select the <div> element
const divElement = document.querySelector('div.float-right.d-none.d-sm-inline');

// Check if the element is found
if (divElement) {
    // Set the display property to 'none' with !important
    divElement.style.setProperty('display', 'none', 'important');
} else {
    console.error('Div element not found');
}

