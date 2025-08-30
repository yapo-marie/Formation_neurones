import { useState } from "react";
import data from "./data";
import "./styles.css";

export default function Accordian() {
  const [selected, setSelected] = useState(null);
  const [enableMultiSelection, setEnableMultiSelection] = useState(false);
  const [multiple, setMultiple] = useState([]);

  const handleSingleSelection = (id) => {
    setSelected(id === selected ? null : id);
  };

  const handleMultiSelection = (id) => {
    const copy = [...multiple];
    const index = copy.indexOf(id);

    if (index === -1) {
      copy.push(id);
    } else {
      copy.splice(index, 1);
    }

    setMultiple(copy);
  };

  const isItemOpen = (id) => {
    return enableMultiSelection ? multiple.includes(id) : selected === id;
  };

  return (
    <div className="acc-wrapper">
      <button onClick={() => setEnableMultiSelection(!enableMultiSelection)}>
        {enableMultiSelection ? "Désactiver multi-sélection" : "Activer multi-sélection"}
      </button>

      <div className="accordion">
        {data.map((item) => (
          <div className="item" key={item.id}>
            <div
              className="title"
              onClick={() =>
                enableMultiSelection
                  ? handleMultiSelection(item.id)
                  : handleSingleSelection(item.id)
              }
            >
              <h3>{item.question}</h3>
              <span>{isItemOpen(item.id) ? "-" : "+"}</span>
            </div>
            {isItemOpen(item.id) && (
              <div className="content">
                <p>{item.answer}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
