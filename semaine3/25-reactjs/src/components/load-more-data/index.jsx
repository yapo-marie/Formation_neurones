import { useEffect, useState, useCallback } from "react";
import "./styles.css";

export default function LoadMoreData() {
  const [loading, setLoading] = useState(false);
  const [products, setProducts] = useState([]);
  const [count, setCount] = useState(0);
  const [disableButton, setDisableButton] = useState(false);

  const fetchProducts = useCallback(async () => {
    try {
      setLoading(true);
      const skip = count * 20;
      const response = await fetch(
        `https://dummyjson.com/products?limit=20&skip=${skip}`
      );

      const result = await response.json();

      if (result?.products?.length > 0) {
        setProducts((prev) => [...prev, ...result.products]);
      }

      if (result?.products?.length < 20 || products.length + result.products.length >= 100) {
        setDisableButton(true);
      }
    } catch (e) {
      console.error("Erreur lors du chargement des produits :", e);
    } finally {
      setLoading(false);
    }
  }, [count, products.length]);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  return (
    <div className="load-more-container">
      {loading && <div>Loading data! Please wait...</div>}

      <div className="product-container">
        {products.map((item) => (
          <div className="product" key={item.id}>
            <img src={item.thumbnail} alt={item.title} />
            <p>{item.title}</p>
          </div>
        ))}
      </div>

      <div className="button-container">
        <button disabled={disableButton} onClick={() => setCount((prev) => prev + 1)}>
          Load More Products
        </button>
        {disableButton && <p>You have reached 100 products.</p>}
      </div>
    </div>
  );
}
