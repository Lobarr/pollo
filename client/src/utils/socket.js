const emit = (event, data) => {
  this.$socket.emit(event, data);
};

export default emit;
