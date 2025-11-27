/**
 * Session Utilities for Project Catalyst
 *
 * Provides project isolation utilities for local-memory integration.
 * CRITICAL: All local-memory operations MUST use session_filter_mode: "session_only"
 */

const fs = require('fs');
const path = require('path');

/**
 * Get the project-specific session ID for isolation enforcement
 *
 * @returns {string} Session ID from .claude/project-session-id
 * @throws {Error} If session ID file is not found or cannot be read
 *
 * Source: https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/README.md
 */
function getProjectSessionId() {
  const projectDir = process.env.CLAUDE_PROJECT_DIR || process.cwd();
  const sessionIdPath = path.join(projectDir, '.claude', 'project-session-id');

  if (!fs.existsSync(sessionIdPath)) {
    throw new Error(
      `🚨 ISOLATION ERROR: Session ID file not found at ${sessionIdPath}\n` +
      `Project isolation requires .claude/project-session-id file.\n` +
      `See: C:\\localmemory\\PROJECT-ISOLATION-SETUP.md`
    );
  }

  try {
    const sessionId = fs.readFileSync(sessionIdPath, 'utf-8').trim();

    if (!sessionId) {
      throw new Error('Session ID file is empty');
    }

    return sessionId;
  } catch (error) {
    throw new Error(
      `🚨 ISOLATION ERROR: Cannot read session ID from ${sessionIdPath}\n` +
      `Error: ${error.message}`
    );
  }
}

/**
 * Get the project name for domain filtering
 *
 * @returns {string} Project name (defaults to 'project-catalyst')
 */
function getProjectName() {
  return 'project-catalyst';
}

/**
 * Verify that local-memory operation parameters include mandatory isolation fields
 *
 * @param {Object} params - Parameters object to validate
 * @throws {Error} If isolation parameters are missing or invalid
 *
 * MANDATORY CHECKS:
 * - session_filter_mode must be "session_only"
 * - session_id must be present
 */
function ensureIsolation(params) {
  if (!params) {
    throw new Error('🚨 ISOLATION VIOLATION: Parameters object is null or undefined');
  }

  if (!params.session_filter_mode || params.session_filter_mode !== 'session_only') {
    throw new Error(
      '🚨 ISOLATION VIOLATION: Must use session_filter_mode: "session_only"\n' +
      `Received: ${JSON.stringify(params.session_filter_mode)}`
    );
  }

  if (!params.session_id) {
    throw new Error(
      '🚨 ISOLATION VIOLATION: Missing session_id parameter\n' +
      'Call getProjectSessionId() to obtain the session ID'
    );
  }

  return true;
}

/**
 * Create a complete local-memory parameters object with mandatory isolation
 *
 * @param {Object} baseParams - Base parameters (content, tags, importance, etc.)
 * @returns {Object} Complete parameters with isolation fields
 *
 * Example:
 *   const params = createIsolatedParams({
 *     content: "Analysis results",
 *     tags: ["project-analysis"],
 *     importance: 8
 *   });
 *   await mcp__local-memory__store_memory(params);
 */
function createIsolatedParams(baseParams) {
  const params = {
    ...baseParams,
    session_filter_mode: 'session_only',
    session_id: getProjectSessionId(),
    domain: getProjectName()
  };

  // Verify before returning
  ensureIsolation(params);

  return params;
}

module.exports = {
  getProjectSessionId,
  getProjectName,
  ensureIsolation,
  createIsolatedParams
};
