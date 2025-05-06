const project_collection_name = "parlamint"
const main_search_field = "full_text"
const search_api_key = "q5A1z9i5OLryOkfnlx3ePGT1wio6MnsI"

const typesenseInstantsearchAdapter = new TypesenseInstantSearchAdapter({
    server: {
        apiKey: search_api_key,
        nodes: [
          /*{
                host: "typesense.acdh-dev.oeaw.ac.at",
                port: "443",
                protocol: "https",
            },
            */      {
                host: "localhost",
                port: "8108",
                protocol: "http",
            }
        ],
    },
    additionalSearchParameters: {
        query_by: main_search_field,
        sort_by: '_text_match:desc, date:asc',
        //rt_by: '_text_match:desc, datum:asc, seite:asc',
    },
});
  
  const searchClient = typesenseInstantsearchAdapter.searchClient;
  
  const indexName = project_collection_name;
  const search = instantsearch({
    searchClient,
    indexName,
    routing: {
      // The stateMapping defines how to map the URL state to the search state and vice-versa
      // currently, only the query parameter is synced
      stateMapping: {
        stateToRoute(uiState) {
          return {
            query: uiState[indexName].query,
          };
        },
        routeToState(routeState) {
          return {
            [indexName]: {
              query: routeState.query
            }
          };
        },
      },
    }
  });
  
  
  function updateHeaderUrl() {
    const searchResult = document.querySelectorAll(".ais-Hits-item");
    const urlParams = new URLSearchParams(window.location.search);
    const queryVal = urlParams.get('query');
    // If search is not empty, update the URL
    if (queryVal.trim() !== '') {
      searchResult.forEach((el) => {
        const urlToUpdate = el.querySelector("h5 a")
        const urlToUpdateHREF = urlToUpdate.getAttribute("href");
        const termToMark = el.querySelector(".ais-Snippet-highlighted").textContent;
        console.log(termToMark);
        let url = new URL(urlToUpdateHREF, window.location.origin);
        let params = new URLSearchParams(url.search);
        // !! Hash (for pages) has to be at the end of the URL !!
        // Remove hash (if any)
        let hash = url.hash;
        url.hash = '';
  
        // Update 'mark' parameter
        params.set('mark', termToMark);
  
        // Set the new search parameters
        url.search = params.toString();
  
        // Add the hash back to the end of the URL
        url.hash = hash;
  
        // Update the href attribute with the relative URL
        // Remove leading slash (if present)
        const newPathname = url.pathname.startsWith('/') ? url.pathname.slice(1) : url.pathname;
        urlToUpdate.setAttribute("href", newPathname + url.search + url.hash);
      });
    }
  }
  
  // Add all widgets
  search.addWidgets([
    instantsearch.widgets.searchBox({
      container: "#searchbox",
      autofocus: true,
      placeholder: 'Suchen',
      cssClasses: {
        form: "form-inline",
        input: "form-control col-md-11",
        submit: "btn",
        reset: "btn",
      },
    }),
  
    instantsearch.widgets.hits({
      container: "#hits",
      cssClasses: {
        item: "w-100"
      },
      templates: {
        empty: "Keine Resultate für <q>{{ query }}</q>",
        item: `
              <h5><a href="{{id}}">{{#helpers.snippet}}{ "attribute": "title", "highlightedTagName": "mark" }{{/helpers.snippet}}</a></h5>
              {{#full_text}}
              <p style="overflow:hidden;max-height:210px;">{{#helpers.snippet}}{ "attribute": "full_text", "highlightedTagName": "mark" }{{/helpers.snippet}}</p>
              {{/full_text}}
            `,
      },
      transformItems(items) {
        return items.map(item => {
          if (search.helper.state.query) {
            return item;
          } else {
            return { ...item, full_text: null };
          }
        });
      },
    }),
  
    instantsearch.widgets.pagination({
      container: "#pagination",
    }),
  
    instantsearch.widgets.clearRefinements({
      container: "#clear-refinements",
      templates: {
        resetLabel: "Filter zurücksetzen",
      },
      cssClasses: {
        button: "btn",
      },
    }),
  
  
    instantsearch.widgets.currentRefinements({
      container: "#current-refinements",
      cssClasses: {
        delete: "btn",
        label: "badge",
      },
    }),
  
    instantsearch.widgets.stats({
      container: "#stats-container",
      templates: {
        text: `
              {{#areHitsSorted}}
                {{#hasNoSortedResults}}keine Treffer{{/hasNoSortedResults}}
                {{#hasOneSortedResults}}1 Treffer{{/hasOneSortedResults}}
                {{#hasManySortedResults}}{{#helpers.formatNumber}}{{nbSortedHits}}{{/helpers.formatNumber}} Treffer {{/hasManySortedResults}}
                aus {{#helpers.formatNumber}}{{nbHits}}{{/helpers.formatNumber}}
              {{/areHitsSorted}}
              {{^areHitsSorted}}
                {{#hasNoResults}}keine Treffer{{/hasNoResults}}
                {{#hasOneResult}}1 Treffer{{/hasOneResult}}
                {{#hasManyResults}}{{#helpers.formatNumber}}{{nbHits}}{{/helpers.formatNumber}} Treffer{{/hasManyResults}}
              {{/areHitsSorted}}
              gefunden in {{processingTimeMS}}ms
            `,
      },
    }),

 instantsearch.widgets.panel({
    collapsed: ({ state }) => {
        return state.query.length === 0;
      },
      templates: {
        header: 'Gesetzgebungsperiode',
      },
    })(instantsearch.widgets.refinementList)({
      container: "#refinement-list-period",
      attribute: "legislative_period",
      templates: {
        showMoreText(data, { html }) {
          return html`<span>${data.isShowingMore ? 'Weniger anzeigen' : 'Mehr anzeigen'}</span>`;
        },
      },
      searchable: true,
      limit: 5,
      showMore: true,
      showMoreLimit: 1000,
      searchablePlaceholder: "Nach Person suchen",
      cssClasses: {
        searchableInput: "form-control form-control-sm m-2 border-light-2",
        searchableSubmit: "d-none",
        searchableReset: "d-none",
        showMore: "btn btn-secondary btn-sm align-content-center",
        list: "list-unstyled",
        count: "badge m-2 badge-secondary",
        label: "d-flex align-items-center text-start",
        checkbox: "m-2",
      },
    }),

    instantsearch.widgets.panel({
      collapsed: ({ state }) => {
        return state.query.length === 0;
      },
      templates: {
        header: 'Personen',
      },
    })(instantsearch.widgets.refinementList)({
      container: "#refinement-list-person",
      attribute: "persons",
      templates: {
        showMoreText(data, { html }) {
          return html`<span>${data.isShowingMore ? 'Weniger anzeigen' : 'Mehr anzeigen'}</span>`;
        },
      },
      searchable: true,
      limit: 5,
      showMore: true,
      showMoreLimit: 1000,
      searchablePlaceholder: "Nach Person suchen",
      cssClasses: {
        searchableInput: "form-control form-control-sm m-2 border-light-2",
        searchableSubmit: "d-none",
        searchableReset: "d-none",
        showMore: "btn btn-secondary btn-sm align-content-center",
        list: "list-unstyled",
        count: "badge m-2 badge-secondary",
        label: "d-flex align-items-center text-start",
        checkbox: "m-2",
      },
    }),
    instantsearch.widgets.panel({
      templates: {
        header: 'Jahr',
      },
    })(instantsearch.widgets.rangeInput)({
      container: "#refinement-range-year",
      attribute: "year",
      templates: {
        separatorText: "bis",
        submitText: "Suchen",
      },
      cssClasses: {
        form: "form-inline",
        input: "form-control",
        submit: "btn",
      },
    }),
    instantsearch.widgets.panel({
        templates: {
          header: 'Datum',
        },
      })(instantsearch.widgets.rangeSlider)({
        container: "#refinement-range-slider",
        attribute: "date",
        templates: {
          //bmitText: "Suchen",
        },
        pips: false,
        cssClasses: {
          form: "form-inline",
          input: "form-control",
          submit: "btn",
        },
      }),
  
    instantsearch.widgets.configure({
      hitsPerPage: 10,
      //attributesToSnippet: [main_search_field],
      attributesToSnippet: ["full_text"],
    }),
  
  ]);
  
  // Add event listener to update the URL
  //  search.on('render', updateHeaderUrl);
  
  search.start();