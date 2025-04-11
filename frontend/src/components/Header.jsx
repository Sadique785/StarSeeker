import React from 'react';
import { useNavigate } from 'react-router-dom';

function Header({ isTransparent = true }) {
  const navigate = useNavigate()
  const handleNavigate = () => {
    navigate('/')
  }
  const headerClass = isTransparent 
    ? "w-full p-4 flex justify-between text-white z-10 absolute top-0 left-0 right-0"
    : "w-full p-4 flex justify-between text-white z-10 bg-black";

  return (
    <header className={headerClass}>
      <div 
      onClick={handleNavigate}
      className="text-2xl font-bold cursor-pointer">Star Seeker</div>
      <nav className="flex items-center space-x-4">

      </nav>
    </header>
  );
}

export default Header;