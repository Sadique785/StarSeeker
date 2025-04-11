import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
// import bgVideo from "../assets/background.mp4";

function Home() {
  return (
    <div className="relative h-screen">
      <video
        autoPlay
        loop
        muted
        className="absolute w-full h-full object-cover"
      >
        {/* <source src={bgVideo} type="video/mp4" /> */}
      </video>

      <div className="absolute inset-0 bg-black bg-opacity-50 flex flex-col items-center justify-center">
        <Header />
        <SearchBar />
      </div>
    </div>
  );
}

export default Home;
