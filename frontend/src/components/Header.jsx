function Header() {
  return (
    <header className="w-full p-4 flex justify-between text-white z-10">
      <div className="text-2xl font-bold">Star Seeker</div>
      <nav className="flex items-center space-x-4">
        <a href="#" className="hover:text-gray-300 transition-colors">Home</a>
        <a href="#" className="hover:text-gray-300 transition-colors">Explore</a>
        <a href="#" className="hover:text-gray-300 transition-colors">About</a>
      </nav>
    </header>
  );
}


export default Header;