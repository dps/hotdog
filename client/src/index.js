// This code was originally based on demo-downshift by Geoff Davis
// https://github.com/geoffdavis92/demo-downshift
import { render } from "react-dom";
import React, { Component } from "react";
import { Div } from "glamorous";
import Downshift from "downshift";

const hotdogs = [
  "addhotdog", "airplane-hotdog", "all-the-hotdogs", "approx-hotdogs", "atlas-hotdog", "az-hotdog-big-0", "az-hotdog-big-1", "az-hotdog-big-2", "az-hotdog-big-3", "behind-seven-hotdogs", "blob-hotdog", "boom-hotdog", "clinking-beer-hotdogs", "cloud-with-hotdogs", "crying-hotdogs", "cute-hotdog", "derp-hotdog", "existential-hotdog-10", "expanding-hotdog-1", "expanding-hotdog-2", "expanding-hotdog-3", "expanding-hotdog-4", "exquisite-hotdog", "fire-hotdog", "future-hotdogs", "global-is-hotdogs", "golden-hotdog", "goodnight-hotdog", "grimacing_face_with_hotdog_for_mouth", "hocho-hotdog", "home_is_where_the_hotdog_is", "honey-bunches-of-hotdogs", "hotdog-0", "hotdog-1", "hotdog-100", "hotdog-2", "hotdog-3", "hotdog-4", "hotdog-5", "hotdog-6", "hotdog-7", "hotdog-8", "hotdog-9", "hotdog-arrival", "hotdog-bow", "hotdog-chair-takedown", "hotdog-confetti-express", "hotdog-countdown-units-0", "hotdog-countdown-units-1", "hotdog-countdown-units-2", "hotdog-countdown-units-3", "hotdog-countdown-units-4", "hotdog-countdown-units-5", "hotdog-countdown-units-6", "hotdog-countdown-units-7", "hotdog-countdown-units-8", "hotdog-countdown-units-9", "hotdog-countup-units-0", "hotdog-countup-units-2", "hotdog-countup-units-3", "hotdog-countup-units-4", "hotdog-countup-units-5", "hotdog-countup-units-6", "hotdog-countup-units-7", "hotdog-countup-units-8", "hotdog-countup-units-9", "hotdog-crying-tears-of-crying-tears-of-hotdogs", "hotdog-crying-tears-of-crying-tears-of-joy", "hotdog-delurk-6", "hotdog-departure", "hotdog-dog", "hotdog-fingerbuns", "hotdog-fingerguns-right", "hotdog-fingerguns", "hotdog-gesturing-no", "hotdog-heart", "hotdog-hotdog", "hotdog-ice-cube", "hotdog-idea", "hotdog-lifting-weights", "hotdog-lurk-18", "hotdog-manager", "hotdog-megaphone", "hotdog-phone", "hotdog-pile", "hotdog-plus", "hotdog-poptart", "hotdog-riding-motorcycle-l", "hotdog-riding-motorcycle-r", "hotdog-riding-scooter-l", "hotdog-riding-scooter-r", "hotdog-riding-scootscoot-l-animated-8", "hotdog-riding-scootscoot-l", "hotdog-riding-scootscoot-r-animated-7", "hotdog-riding-scootscoot-r", "hotdog-save-o-meter-peek", "hotdog-shocked", "hotdog-shrugging", "hotdog-snapchat", "hotdog-snowboarder", "hotdog-teacher", "hotdog-text", "hotdog-waiting-0", "hotdog-waiting-1", "hotdog-with-monacle", "hotdog-yes", "hotdog-yes2", "hotdog_face", "hotdog_food_pls", "hotdog_roller_coaster", "hotdoge", "hotdogjack", "hotdogpeek", "hotdogs-crossed", "hotdogtld", "irc-hotdog", "kosher-hotdog", "lacroix-hotdog", "lhotdog", "llama-hotdog-1", "llama-nibbles-hotdog-0", "look-of-hotdog", "morning-hotdog", "night-hotdog", "not-the-hotdogs-youre-looking-for", "obama-hotdog", "ohno-hotdog", "panda-eating-hotdog", "party_try_not_to_hotdog-0", "party_try_not_to_hotdog-1", "party_try_not_to_hotdog-10", "party_try_not_to_hotdog-13", "party_try_not_to_hotdog-14", "party_try_not_to_hotdog-15", "party_try_not_to_hotdog-2", "party_try_not_to_hotdog-3", "party_try_not_to_hotdog-4", "party_try_not_to_hotdog-5", "party_try_not_to_hotdog-6", "party_try_not_to_hotdog-7", "party_try_not_to_hotdog-8", "party_try_not_to_hotdog-9", "patrick_hotdog", "person-raising-hotdog", "plus-hotdog", "popcorn-hotdog", "praise-the-hotdogs", "pray-hotdog", "raised-hotdogs", "rip-hotdog", "saddest-hotdog", "saddest-panda-hotdog", "salon-hotdog", "see-no-evil-hotdog", "shakes-hotdog", "shitty_chart_with_hotdog_trend_screenshot", "skiing-hotdog", "slack-hotdog-bottom-left", "slack-hotdog-bottom-right", "slack-hotdog-top-left", "slack-hotdog-top-right", "smiling-hotdog-but-dead-inside", "smiling-hotdog", "snowboarding-hotdog", "sparkles-hotdog-end", "sparkles-hotdog", "speedboat-hotdog", "spooky-zombie-hotdog", "squish-hotdog-0", "squish-hotdog-28", "teamwork_makes_the_hotdog_work", "thanks-hotdog", "thinking_hotdog", "this-is-fine-hotdog", "try_not_to_hotdog-0", "turing-complete-hotdog", "umbrella-with-hotdogs", "urgency-and-hotdog", "wave-hotdog", "wtb-hotdogs", "ylukem-hotdog"
];

const NO_RESULTS = "outta hotdogs";

const SpectreItem = ({ children, value, index, isActive, onClick }) => (
  <div
    className="menu-item"
    style={isActive ? { backgroundColor: "#eee" } : {}}
    onClick={onClick}
  >
    <a href="#!">
      <div className="tile tile-centered">
        <figure className="avatar avatar-sm" style={{ backgroundColor: "#fff" }} >
          <img src={"/imgs/hotdogs/" + children + ".png"} alt={value} />
        </figure>
        <div className="tile-content">{children}</div>
      </div>
    </a>
  </div>
);

class SpectreAutocomplete extends Component {
  constructor() {
    super();
    this.promoDog = hotdogs[Math.floor(Math.random() * hotdogs.length)]
    this.state = {
      selectedHotdogs: [],
      availableHotdogs: [...hotdogs],
      lastSelected: this.promoDog
    };
    this.addHotdog = this.addHotdog.bind(this);
    this.removeHotdog = this.removeHotdog.bind(this);
    this.clearInputValue = this.clearInputValue.bind(this);
    this.keyboardChange = this.keyboardChange.bind(this);
  }
  toVal(g) {
    return g.value;
  }
  componentDidMount() {
    window.addEventListener("keydown", ({ keyCode }) => {
      if (
        keyCode === 8 &&
        this.ACInput.value === "" &&
        this.state.selectedHotdogs.length >= 1
      ) {
        this.setState(prevState => {
          const { selectedHotdogs } = prevState;
          const editableSelectedHotdogs = [...selectedHotdogs];
          editableSelectedHotdogs.splice(-1, 1);
          return {
            selectedHotdogs: editableSelectedHotdogs
          };
        });
      }
    });
    this.ACInput.addEventListener("keydown", ({ keyCode }) => {
      if (
        keyCode === 13 &&
        this.ACInput.value === "" &&
        this.state.selectedHotdogs.length >= 1
      ) {
        window.location.href =
          "/shipping?" +
          this.state.selectedHotdogs
            .map(({ hotdog, availableHotdogsIndex }, i) => {
              return hotdog;
            })
            .join(",");
      }
    });
  }
  clearInputValue() {
    this.downshift.clearSelection();
  }
  addHotdog({ value, index }, callback) {
    if (value === NO_RESULTS) {
      if (callback) {
        callback();
      }
      return;
    }
    this.setState(
      prevState => {
        const availableHotdogs = [...prevState.availableHotdogs];
        const selectedHotdogs = [...prevState.selectedHotdogs];

        selectedHotdogs.push({ hotdog: value, availableHotdogsIndex: index });
        const lastSelected = value;

        return {
          selectedHotdogs,
          availableHotdogs,
          lastSelected
        };
      },
      () => {
        if (callback) {
          callback();
        }
      }
    );
  }
  removeHotdog({ value, index, availableHotdogsIndex }) {
    this.setState(prevState => {
      const availableHotdogs = [...prevState.availableHotdogs];
      const selectedHotdogs = [...prevState.selectedHotdogs];
      const lastSelected = prevState.lastSelected;

      availableHotdogs.splice(availableHotdogsIndex, 0, value);
      selectedHotdogs.splice(index, 1);

      return {
        selectedHotdogs,
        availableHotdogs,
        lastSelected
      };
    });
  }
  clickChange(item, clearSelection) {
    this.addHotdog(
      {
        value: item,
        index: this.state.availableHotdogs.indexOf(item)
      },
      clearSelection
    );
  }
  keyboardChange(hotdog, clearSelection) {
    hotdog !== null &&
      this.addHotdog(
        {
          value: hotdog,
          index: this.state.availableHotdogs.indexOf(hotdog)
        },
        this.downshift.clearSelection
      );
  }
  render() {
    const selectedHotdogTags = this.state.selectedHotdogs.map(
      ({ hotdog, availableHotdogsIndex }, i) => {
        return (
          <label className="chip" key={hotdog}>
            <b>
              {
                this.state.selectedHotdogs.filter(v => {
                  return v.hotdog === hotdog;
                }).length
              }
              x
            </b>&nbsp;
            {hotdog}
            <button
              className="btn btn-clear"
              onClick={({ target }) => {
                this.removeHotdog({
                  value: hotdog,
                  index: i,
                  availableHotdogsIndex
                });
              }}
            />
          </label>
        );
      }
    );
    return (
      <Downshift
        ref={downshift => (this.downshift = downshift)}
        onChange={hotdog => this.keyboardChange(hotdog)}
      >
        {({
          clearSelection,
          getDownshiftStateAndHelpers,
          getInputProps,
          getItemProps,
          setInputProps,
          isOpen,
          inputValue,
          selectedItem,
          highlightedIndex
        }) => (
          <div>
            <div className="form-autocomplete-input form-input">
              {selectedHotdogTags}
              <input
                defaultValue=""
                {...getInputProps({
                  defaultValue: ""
                })}
                className="form-input"
                type="text"
                placeholder={this.promoDog}
                ref={n => (this.ACInput = n)}
              />
              {(isOpen && (
                <div className="menu">
                  {(() => {
                    let filterMatchCount = 0;
                    return [...this.state.availableHotdogs, NO_RESULTS]
                      .filter((currentItem, index, allAvailableHotdogs) => {
                        if (
                          currentItem !==
                          allAvailableHotdogs[allAvailableHotdogs.length - 1]
                        ) {
                          filterMatchCount +=
                            currentItem !== null &&
                            (!inputValue ||
                              currentItem
                                .toLowerCase()
                                .includes(inputValue.toLowerCase()))
                              ? 1
                              : 0;
                          return (
                            currentItem !== null &&
                            currentItem !== NO_RESULTS &&
                            (!inputValue ||
                              currentItem
                                .toLowerCase()
                                .includes(inputValue.toLowerCase()))
                          );
                        } else if (
                          currentItem ===
                            allAvailableHotdogs[
                              allAvailableHotdogs.length - 1
                            ] &&
                          filterMatchCount <= 0
                        ) {
                          return true;
                        }
                      })
                      .map((item, index, arr) => (
                        <SpectreItem
                          {...getItemProps({ item, index })}
                          key={item}
                          isActive={highlightedIndex === index}
                          onClick={() =>
                            this.clickChange(item, clearSelection)
                          }
                        >
                          {item}
                        </SpectreItem>
                      ));
                  })()}
                </div>
              )) ||
                (!isOpen && <div />)}
            </div>
            {(this.state.selectedHotdogs.length > 0 &&
            <a
              href={
                "/shipping?" +
                  this.state.selectedHotdogs.map(({ hotdog, availableHotdogsIndex }, i) => {return hotdog;}).join(",")
              }
            >
              <button className="btn btn-primary" style={{marginTop: `4px`}}>
                Buy ${12 * this.state.selectedHotdogs.length} &rarr;
              </button>
            </a>
            )}
              <center>
                <img
                  style={{ margin: "auto", maxWidth: 600 }}
                  src={"/imgs/previews/" + this.state.lastSelected + ".png"}
                />
              </center>
          </div>
        )}

      </Downshift>
    );
  }
}

const Preview = () => {
  return (
    <img src="https://images.printify.com/mockup/5ca12035dd4f73b947055283/45153/1535/?s=400&t=1554063417000" />
  );
}
const Examples = () => {
  return (
    <Div>
      <link
        href="https://unpkg.com/spectre.css@0.2.14/dist/spectre.css"
        rel="stylesheet"
      />
      <link
        href="https://unpkg.com/spectre.css@0.2.14/dist/spectre-icons.css"
        rel="stylesheet"
      />
      <div
        className="form-autocomplete"
        style={{ margin: "auto", maxWidth: 600 }}
      >
        <SpectreAutocomplete />
      </div>
    </Div>
  );
};

render(<Examples />, document.getElementById("react"));
