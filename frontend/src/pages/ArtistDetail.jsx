import { useParams } from "react-router-dom";

function ArtistDetail() {
  const { id } = useParams();

  return (
    <div className="p-8 text-white">
      <h1 className="text-3xl">Artist Detail Page</h1>
      <p>Artist ID: {id}</p>
    </div>
  );
}

export default ArtistDetail;
