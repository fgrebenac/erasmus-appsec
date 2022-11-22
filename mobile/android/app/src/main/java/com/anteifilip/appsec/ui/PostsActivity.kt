package com.anteifilip.appsec.ui

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.isVisible
import com.anteifilip.appsec.databinding.ActivityNotesBinding
import com.anteifilip.appsec.utils.PreferenceHelper
import com.anteifilip.appsec.utils.PreferenceHelper.get
import com.anteifilip.appsec.utils.onClickDebounced
import com.anteifilip.appsec.utils.viewBinding
import org.koin.androidx.viewmodel.ext.android.viewModel

class PostsActivity : AppCompatActivity() {

    private val binding by viewBinding(ActivityNotesBinding::inflate)
    private val viewModel: AppSecViewModel by viewModel()
    private lateinit var adapter: PostsAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)
        observeViewModel()
        initViews()
        viewModel.getPosts(PreferenceHelper.defaultPrefs(this)["userId"])
    }

    private fun initViews() {
        binding.addNoteButton.onClickDebounced {
            val dialog = NewPostDialogFragment {
                viewModel.getPosts(PreferenceHelper.defaultPrefs(this)["userId"])
            }
            dialog.show(supportFragmentManager, "NewPostDialog")
        }
        binding.swipe.setOnRefreshListener {
            viewModel.getPosts(PreferenceHelper.defaultPrefs(this)["userId"])
        }
    }

    private fun observeViewModel() {
        viewModel.getPostsResponse.observe(this) {
            adapter = PostsAdapter(it, { post ->
                val dialog = NewPostDialogFragment(post) {
                    viewModel.getPosts(PreferenceHelper.defaultPrefs(this)["userId"])
                }
                dialog.show(supportFragmentManager, "NewPostDialog")
            }, { post ->
                viewModel.deletePost(PreferenceHelper.defaultPrefs(this)["userId"], post.id)
            })
            binding.notesRecyclerView.adapter = adapter
            binding.swipe.isRefreshing = false
            binding.noNotesLayout.isVisible = it.isEmpty()
        }
        viewModel.getPostsError.observe(this) {
            Toast.makeText(this, "Failed to get posts.", Toast.LENGTH_SHORT).show()
            binding.noNotesLayout.isVisible = true
        }
        viewModel.deletePostResponse.observe(this) {
            viewModel.getPosts(PreferenceHelper.defaultPrefs(this)["userId"])
        }
        viewModel.deletePostError.observe(this) {
            Toast.makeText(this, "Failed to delete post.", Toast.LENGTH_SHORT).show()
        }
    }

}