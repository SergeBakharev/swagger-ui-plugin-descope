import React from "react"
import PropTypes from "prop-types"


export default class DescopeAuthorizationPopup extends React.Component {
  close =() => {
    let { authActions } = this.props

    authActions.showDefinitions(false)
  }

  componentDidMount() {
      descope_sdk.refresh().then(() => {
        var container = document.getElementById('descope-container');

        let { getConfigs, getComponent, errSelectors, schema } = this.props

        const projectId = getConfigs().descopeProjectId
        const flowId = getConfigs().descopeFlowId

        const sessionToken = descope_sdk.getSessionToken()
        var notValidToken

        if (sessionToken) {
            notValidToken = descope_sdk.isJwtExpired(sessionToken)
        }

        if (sessionToken || !notValidToken) {
          container.innerHTML = '<button class="btn modal-btn auth button" onclick="descope_sdk.logout().then(()=>{location.reload();})">Logout</button>';
          const HttpAuth = getComponent("HttpAuth")
          HttpAuth.value = sessionToken
        }

        if (!sessionToken || notValidToken) {
          container.innerHTML = `<descope-wc project-id='${projectId}' flow-id='${flowId}'></descope-wc>`;

          const wcElement = document.getElementsByTagName('descope-wc')[0];
          const onSuccess = (e) => {
            console.log("successfully authed")
            console.log(e.detail.user),
            descope_sdk.refresh()
            location.reload()
          };
          const onError = (err) => console.log(err);

          wcElement.addEventListener('success', onSuccess);
          wcElement.addEventListener('error', onError);
        }

    })
  }

  render() {
    let { authSelectors, authActions, getComponent, errSelectors, specSelectors, fn: { AST = {} } } = this.props
    let definitions = authSelectors.shownDefinitions()
    const Auths = getComponent("auths")
    const CloseIcon = getComponent("CloseIcon")
    const Button = getComponent("Button")

    return (
      <div className="dialog-ux">
        <div className="backdrop-ux"></div>
        <div className="modal-ux">
          <div className="modal-dialog-ux">
            <div className="modal-ux-inner">
              <div className="modal-ux-header">
                <h3>Log In With Descope Flows</h3>
                <button type="button" className="close-modal" onClick={ this.close }>
                  <CloseIcon />
                </button>
              </div>
              <div className="modal-ux-content">
                <div class="auth-container"><h4>Descope Auth</h4>
                <p id="descope-container"></p>
              </div>
                <p>Or provide a Token:</p>
                {
                  definitions.valueSeq().map(( definition, key ) => {
                    return <Auths key={ key }
                                  AST={AST}
                                  definitions={ definition }
                                  getComponent={ getComponent }
                                  errSelectors={ errSelectors }
                                  authSelectors={ authSelectors }
                                  authActions={ authActions }
                                  specSelectors={ specSelectors }/>
                  })
                }                
                <Button className="btn modal-btn auth btn-done" onClick={ this.close }>Close</Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  static propTypes = {
    fn: PropTypes.object.isRequired,
    getComponent: PropTypes.func.isRequired,
    authSelectors: PropTypes.object.isRequired,
    specSelectors: PropTypes.object.isRequired,
    errSelectors: PropTypes.object.isRequired,
    authActions: PropTypes.object.isRequired,
  }
}
