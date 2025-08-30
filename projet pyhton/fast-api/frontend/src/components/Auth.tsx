import { useLocation, Navigate } from "react-router-dom";
import type { ReactNode } from "react";


export const setToken = (token: string) => {
  localStorage.setItem("temitope", token);
};


export const fetchToken = (): string | null => {
  return localStorage.getItem("temitope");
};

interface RequireTokenProps {
  children: ReactNode;
}

export function RequireToken({ children }: RequireTokenProps) {
  const auth = fetchToken();
  const location = useLocation();

  if (!auth) {
    return <Navigate to="/" state={{ from: location }} />;
  }

  return <>{children}</>;
}
