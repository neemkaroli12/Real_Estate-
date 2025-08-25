// // Get slider track
// const track = document.getElementById('sliderTrack');

// // Buttons
// const prevBtn = document.querySelector('.prev-btn');
// const nextBtn = document.querySelector('.next-btn');

// // Slider state
// let slideIndex = 0;
// const slideWidth = 170; // One slide width + margin

// function moveSlider(direction) {
//   const wrapper = document.querySelector('.slider-wrapper');
//   const totalSlides = track.children.length;
//   const visibleSlides = Math.floor(wrapper.offsetWidth / slideWidth);
//   const maxScroll = (totalSlides * slideWidth) - wrapper.offsetWidth;

//   // Update index
//   slideIndex += direction;
//   if (slideIndex < 0) slideIndex = 0;

//   const maxIndex = Math.ceil(maxScroll / slideWidth);
//   if (slideIndex > maxIndex) slideIndex = maxIndex;

//   // Calculate move amount safely
//   let moveAmount = slideIndex * slideWidth;
//   if (moveAmount > maxScroll) {
//     moveAmount = maxScroll;
//   }

//   track.style.transform = `translateX(-${moveAmount}px)`;

//   // Update button visibility
//   updateButtons(moveAmount, maxScroll);
// }

// function updateButtons(currentScroll, maxScroll) {
//   prevBtn.style.display = currentScroll <= 0 ? 'none' : 'block';
//   nextBtn.style.display = currentScroll >= maxScroll ? 'none' : 'block';
// }

// // Initialize on page load
// window.addEventListener('DOMContentLoaded', () => {
//   const wrapper = document.querySelector('.slider-wrapper');
//   const totalSlides = track.children.length;
//   const visibleSlides = Math.floor(wrapper.offsetWidth / slideWidth);
//   const maxScroll = (totalSlides * slideWidth) - wrapper.offsetWidth;

//   updateButtons(0, maxScroll);
// });
const track = document.getElementById("sliderTrack");
const prevBtn = document.querySelector(".prev-btn");
const nextBtn = document.querySelector(".next-btn");
const wrapper = document.querySelector(".slider-wrapper");

let currentPosition = 0;

function getSlideWidth() {
  const slide = document.querySelector(".slide");
  const style = window.getComputedStyle(slide);
  const width = slide.offsetWidth;
  const marginRight = parseInt(style.marginRight);
  return width + marginRight;
}

function moveSlider(direction) {
  const slideWidth = getSlideWidth();
  const maxScroll = track.scrollWidth - wrapper.offsetWidth;

  currentPosition += direction * slideWidth;

  if (currentPosition < 0) currentPosition = 0;
  if (currentPosition > maxScroll) currentPosition = maxScroll;

  track.style.transform = `translateX(-${currentPosition}px)`;

  prevBtn.style.display = currentPosition <= 0 ? "none" : "block";
  nextBtn.style.display = currentPosition >= maxScroll ? "none" : "block";
}

window.addEventListener("DOMContentLoaded", () => {
  moveSlider(0);
});
