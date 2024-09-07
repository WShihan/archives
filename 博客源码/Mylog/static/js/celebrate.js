function celebrate() {
  /* 🎉 */
  var triangle = confetti.shapeFromPath({ path: 'M0 10 L5 0 L10 10z' });
  confetti({
    shapes: [triangle],
  });
}
