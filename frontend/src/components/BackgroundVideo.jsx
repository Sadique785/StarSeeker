import React from 'react'

const BackgroundVideo = () => {
  return (
    <div className="absolute inset-0 z-0">
    <video 
      autoPlay 
      loop 
      muted 
      className="object-cover w-full h-full"
      poster="images/backup.jpg"
    >
      <source src='videos/video3.mp4' type="video/mp4" />
      Your browser does not support the video tag.
    </video>
    
    {/* Overlay gradient for better text readability */}
    <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/40 to-black/70"></div>
  </div>
  )
}

export default BackgroundVideo