TIMESTAMP_FORMAT="+%Y-%m-%d %H:%M:%S"

function _log () {
    echo $(date "$TIMESTAMP_FORMAT"): $RUN_ID: $@
}

function _log_boxed () {
    _log ---------------------------------
    _log $@
    _log ---------------------------------
}
