import { useEffect, useState, useCallback } from "react";

export default function useFetch(url, options = {}) {
  const [data, setData] = useState(null);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    setPending(true);
    try {
      const response = await fetch(url, { ...options });
      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      const result = await response.json();
      setData(result);
      setError(null);
    } catch (e) {
      setError(`${e.message}. An error occurred.`);
      setData(null);
    } finally {
      setPending(false);
    }
  }, [url, options]);

  useEffect(() => {
    if (url) {
      fetchData();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fetchData]);

  return { data, error, pending };
}
