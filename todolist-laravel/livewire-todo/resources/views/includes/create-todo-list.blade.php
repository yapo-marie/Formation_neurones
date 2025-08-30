<div class="container content py-6 mx-auto create-todo">
    <div class="mx-auto div">
        <div class="hover:shadow p-5 bg-white border-blue-500 border-t-2">
            <div class="flex">
                <h2 class="text-lg text-gray-800 mb-4">Create New Todo</h2>
            </div>
            <div>
                <form>
                    <div class="mb-5">
                        <label for="title" class="block mb-3 text-sm font-medium text-gray-900 dark:text-white">*
                            Todo </label>
                        <input wire:model="name" type="text" id="title" placeholder=".." class="bg-gray-100  text-gray-800 text-sm rounded block w-full p-3">
                        @error('name')
                            <span class="text-red-500 text-xs mt-4 block ">{{ $message }}</span>
                        @enderror
                    </div>
                    <button wire:click.prevent="create" type="submit" class="px-4 py-3 bg-blue-500 text-white rounded hover:bg-blue-600">Create
                        +</button>
                    @if (session('success'))
                        <span class="text-green-600 text-xs">{{ session('success') }}</span>
                    @endif
                </form>
            </div>
        </div>
    </div>
</div>