import { useEffect, useState, useCallback } from "react";
import {
  BsArrowLeftCircleFill,
  BsArrowRightCircleFill,
} from "react-icons/bs";
import "./styles.css";

export default function ImageSlider({ url, limit = 5, page = 1 }) {
  const [images, setImages] = useState([]);
  const [currentSlide, setCurrentSlide] = useState(0);
  const [errorMsg, setErrorMsg] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchImages = useCallback(async () => {
    if (!url) return;
    setLoading(true);
    setErrorMsg(null);

    try {
      const response = await fetch(`${url}?page=${page}&limit=${limit}`);
      if (!response.ok) {
        throw new Error("Erreur lors du chargement des images.");
      }

      const data = await response.json();
      if (Array.isArray(data)) {
        setImages(data);
      } else {
        throw new Error("Réponse inattendue de l'API.");
      }
    } catch (e) {
      setErrorMsg(e.message);
    } finally {
      setLoading(false);
    }
  }, [url, page, limit]);

  useEffect(() => {
    fetchImages();
  }, [fetchImages]);

  const handlePrevious = () => {
    setCurrentSlide((prev) =>
      prev === 0 ? images.length - 1 : prev - 1
    );
  };

  const handleNext = () => {
    setCurrentSlide((prev) =>
      prev === images.length - 1 ? 0 : prev + 1
    );
  };

  if (loading) return <div>Loading images... Please wait.</div>;
  if (errorMsg) return <div>Error occurred: {errorMsg}</div>;

  return (
    <div className="container">
      <BsArrowLeftCircleFill
        onClick={handlePrevious}
        className="arrow arrow-left"
      />

      {images.length > 0 &&
        images.map((imageItem, index) => (
          <img
            key={imageItem.id}
            alt={imageItem.author || "slide"}
            src={imageItem.download_url}
            className={
              currentSlide === index
                ? "current-image"
                : "current-image hide-current-image"
            }
          />
        ))}

      <BsArrowRightCircleFill
        onClick={handleNext}
        className="arrow arrow-right"
      />

      <span className="circle-indicators">
        {images.length > 0 &&
          images.map((_, index) => (
            <button
              key={index}
              className={
                currentSlide === index
                  ? "current-indicator"
                  : "current-indicator inactive-indicator"
              }
              onClick={() => setCurrentSlide(index)}
            ></button>
          ))}
      </span>
    </div>
  );
}
