function AnimatedTransition({ show, children }) {
    return (
      <div className={`transition-all duration-300 ${
        show ? 'opacity-100 max-h-screen' : 'opacity-0 max-h-0'
      }`}>
        {children}
      </div>
    );
  }
  export default AnimatedTransition;